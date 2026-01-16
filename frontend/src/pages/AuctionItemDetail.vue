<template>
  <div class="auction-item-detail">

    <!-- ITEM LOADED -->
    <div v-if="item">

      <div class="item-card">
        <h1 class="item-title">{{ item.title }}</h1>

        <img v-if="item.imageUrl" :src="item.imageUrl" class="item-image" />
        <img v-else :src="placeholderUrl" class="item-image" />

        <div class="item-info">
          <p><strong>Description:</strong> {{ item.description }}</p>
          <p><strong>Starting Bid:</strong> ${{ item.startingBid.toFixed(2) }}</p>
          <p :class="{ 'bid-flash': bidUpdated }">
            <strong>Current Bid:</strong> ${{ item.currentBid.toFixed(2) }}
          </p>
          <p><strong>Auction Ends:</strong> {{ formatEndDate(item.endDate) }}</p>
        </div>
      </div>

      <!-- PLACE BID -->
      <div class="place-bid">
        <input type="number" v-model.number="newBid" />
        <button
          @click="submitBid"
          :disabled="!newBid || newBid <= item.currentBid"
        >
          Submit Bid
        </button>
        <p v-if="bidError">{{ bidError }}</p>
      </div>

      <!-- QUESTIONS -->
      <div class="item-questions">
        <h2>Questions & Answers</h2>
        <!--<p>DEBUG owner: {{ item.ownerUsername }}</p>
        <p>DEBUG current: {{ currentUser }}</p>-->

        <div v-if="questions.length === 0">
          <p>No questions yet.</p>
        </div>

        <div v-else>
          <div v-for="question in questions" :key="question.id">
            <p><strong>Q:</strong> {{ question.question_text }}</p>

            <p v-if="question.answer_text">
              <strong>A:</strong> {{ question.answer_text }}
            </p>

            <div v-else-if="item.ownerUsername === currentUser">
              <form @submit.prevent="submitAnswer(question)">
                <textarea v-model="question.newAnswer"></textarea>
                <button>Answer</button>
              </form>
            </div>

            <div v-else>
              <em>This question has not been answered yet.</em>
            </div>
          </div>
        </div>
      </div>

      <!-- ASK QUESTION -->
      <div class="ask-question">
        <form @submit.prevent="submitQuestion">
          <textarea v-model="newQuestion"></textarea>
          <button type="submit">Ask Question</button>
        </form>
        <p v-if="questionError">{{ questionError }}</p>
      </div>

    </div>

    <!-- LOADING -->
    <p v-else class="loading">Loading item details...</p>

    <!-- ERROR -->
    <p v-if="fetchError">{{ fetchError }}</p>

  </div>
</template>


<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useAuctionStore, AuctionItem } from '../stores/auctionStore';

export default defineComponent({
    name: 'AuctionItemDetail',
    setup() {
        const auctionStore = useAuctionStore();
        const route = useRoute();
        const itemId = Number(route.params.id);

        const item = computed(() => auctionStore.getItem(itemId));

        const questions = ref<any[]>([]);
        const placeholderUrl = '/static/api/spa/assets/placeholder.jpg';
        const newQuestion = ref('');
        const questionError = ref('');
        const fetchError = ref('');
        const newBid = ref<number | null>(null);
        const bidError = ref('');
        const bidUpdated = ref(false);


        function getCookie(name: string): string | null {
            const match = document.cookie.match(new RegExp("(^|; )" + name + "=([^;]*)"));
            return match ? decodeURIComponent(match[2]) : null;
        }

        const formatEndDate = (end: string) => {
            const endDate = new Date(end);
            return endDate.toLocaleString();
        };

        const fetchItemDetails = async (id: number) => {
            try {
                const response = await fetch(`/api/auction-items/${id}/`);
                const data = await response.json();

                const updatedItem: AuctionItem = {
                    id: data.id,
                    title: data.title,
                    description: data.description,
                    startingBid: parseFloat(data.starting_bid),
                    currentBid: data.current_bid ? parseFloat(data.current_bid) : 0,
                    imageUrl: data.image,
                    endDate: data.end_datetime,
                    ownerUsername: data.ownerUsername
                };

                auctionStore.setItem(updatedItem); //only update store
            } catch (error) {
                fetchError.value = 'Failed to load item details.';
                console.error(error);
            }
        };

        const fetchQuestions = async (itemId: number) => {
        try {
            const response = await fetch(`/api/item-questions/?item_id=${itemId}`);
            if (!response.ok) throw new Error('Failed to fetch questions');
            questions.value = await response.json();
        } catch (error) {
            console.error(error);
        }
    };

    const currentUser = ref<string | null>(null);
    const fetchCurrentUser = async () => {
        try {
            const response = await fetch(
                '/api/current-user/',
                {
                    credentials: 'same-origin'
                }
            );
            if (!response.ok) throw new Error('Failed to fetch current user');
            const data = await response.json();
            currentUser.value = data.username;
        } catch (error) {
            console.error(error);
        }
    };

    const submitQuestion = async () => {
        if (!item.value || !newQuestion.value.trim()) return;

        const csrfToken = getCookie('csrftoken');

        try {
            const response = await fetch(`/api/item-questions/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...(csrfToken ? { "X-CSRFToken": csrfToken } : {}),
                },
                body: JSON.stringify({
                    item: item.value.id,
                    question_text: newQuestion.value,
                })
            });

            if (!response.ok) {
                const errText = await response.text();
                throw new Error(errText);
            }


            const createdQuestion = await response.json();
            questions.value.push(createdQuestion); // update list immediately
            newQuestion.value = '';
            questionError.value = '';

            fetchQuestions(item.value.id);

        } catch (error) {
            questionError.value = (error as Error).message;
        }
    };

    const submitAnswer = async (question: any) => {
        if (!question.newAnswer?.trim()) return;

        const csrfToken = getCookie('csrftoken');

        try {
            const response = await fetch(
            `/api/item-questions/${question.id}/answer/`,
            {
                method: 'PATCH',
                headers: {
                'Content-Type': 'application/json',
                ...(csrfToken ? { "X-CSRFToken": csrfToken } : {})
                },
                body: JSON.stringify({
                answer_text: question.newAnswer
                })
            }
            );

            if (!response.ok) throw new Error('Failed to submit answer');

            const updated = await response.json();

            question.answer_text = updated.answer_text;
            question.newAnswer = '';

        } catch (err) {
            console.error(err);
        }
    };


    const submitBid = async () => {
        if (!item.value || newBid.value === null) return;

        const csrfToken = getCookie('csrftoken');

        const formData = new FormData();
        formData.append('bid_amount', newBid.value!.toString());

        try {
            const response = await fetch(
                `/api/auction-items/${item.value.id}/place_bid/`,
                {
                    method: 'POST',
                    body: formData,
                    credentials: 'same-origin',
                    headers: csrfToken ? { 'X-CSRFToken': csrfToken } : {}
                }
            );

            const data = await response.json().catch(() => ({}));

            if (!response.ok) {
                throw new Error(data.error || 'Failed to place bid.');
            }

            const updatedItem = data;

            auctionStore.updateBid(item.value.id, parseFloat(updatedItem.current_bid));

            newBid.value = null;
            bidError.value = '';
            bidUpdated.value = true;
            setTimeout(() => (bidUpdated.value = false), 1200);

        } catch (err) {
            bidError.value = (err as Error).message;
        }
    };



        onMounted(() => {
            const itemId = Number(route.params.id);
            if (!isNaN(itemId)) {
                fetchItemDetails(itemId);
                fetchQuestions(itemId);
                fetchCurrentUser();
            }
        });

        return {
            item,
            currentUser,
            placeholderUrl,
            formatEndDate,
            newQuestion,
            questionError,
            submitQuestion,
            questions,
            fetchError,
            submitAnswer,
            newBid,
            bidError,
            submitBid,
            bidUpdated
        };
    }
});

</script>

<style scoped>
.auction-item-detail {
    max-width: 800px;
    margin: 40px auto;
    padding: 20px;
}

.item-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}


.item-title {
    font-size: 28px;
    margin-bottom: 20px;
    text-align: center;
    }

.item-image {
    display: block;
    width: 100%;
    max-height: 400px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 20px;
}

.item-info p {
    margin-bottom: 10px;
    line-height: 1.5;
    font-size: 16px;
}

.item-info .description {
    color: #555;
}

.item-info .price {
    font-weight: bold;
    color: #1a73e8;
}

.item-info .end-time {
    font-size: 14px;
    color: #888;
}

.loading {
    font-size: 18px;
    text-align: center;
    margin-top: 40px;
}

.item-questions {
    margin-top: 30px;
    border-top: 1px solid #ddd;
    padding-top: 20px;
}

.item-questions h2 {
    font-size: 22px;
    margin-bottom: 15px;
    text-align: center;
}

.question-item {
    border: 1px solid #eee;
    border-radius: 6px;
    padding: 12px 15px;
    margin-bottom: 12px;
    background-color: #fafafa;
}

.question-item p {
    margin: 4px 0;
    font-size: 15px;
}

.ask-question {
    margin-top: 20px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
}

.ask-question h3 {
    margin-bottom: 10px;
    font-size: 18px;
}

.question-input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 14px;
    margin-bottom: 10px;
    resize: vertical;
}

.ask-question button {
    background-color: #1a73e8;
    color: #fff;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.2s ease;
}

.ask-question button:hover {
    background-color: #155ab6;
}
.error-message {
    color: red;
    margin-top: 40px;
    text-align: center;
}

.answer-box {
    margin-top: 8px;
}

.answer-box textarea {
    width: 100%;
    padding: 6px;
    margin-bottom: 6px;
}

.answer-form button {
    background-color: #34a853;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
}

.answer-form button:hover {
    background-color: #2c8c47;
}

.place-bid-title {
    margin-top: 20px;
}

.bid-input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 14px;
    margin-bottom: 10px;
    box-sizing: border-box;
}

.bid-button {
    background-color: #1a73e8;
    color: #fff;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.2s ease;
}

.bid-button:hover {
    background-color: #155ab6;
}

.bid-button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

.bid-flash {
  display: inline-block; /* ensures scaling doesn't push content */
  animation: bidPop 0.6s ease-in-out;
}

@keyframes bidPop {
  0%, 100% {
    color: #1a73e8;   /* normal blue */
    transform: scale(1); 
  }
  50% {
    color: #28a745;   /* flash green */
    transform: scale(1.2); /* slightly bigger */
    font-weight: bold;
  }
}

</style>
