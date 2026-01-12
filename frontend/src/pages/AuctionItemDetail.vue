<template>

    <div class="auction-item-detail" v-if="item">
        <div class="item-card">
            <h1 class="item-title">{{ item.title }}</h1>

            <img
            v-if="item.imageUrl"
            :src="item.imageUrl"
            alt="Auction Item Image"
            class="item-image"
            />
            <img
            v-else
            :src="placeholderUrl"
            alt="Placeholder Image"
            class="item-image"
            />

            <div class="item-info">
            <p class="description"><strong>Description:</strong> {{ item.description }}</p>
            <p class="price"><strong>Starting Bid:</strong> ${{ item.startingBid.toFixed(2) }}</p>
            <p class="price"><strong>Current Bid:</strong> ${{ item.currentBid.toFixed(2) }}</p>
            <p class="end-time"><strong>Auction Ends:</strong> {{ formatEndDate(item.endDate) }}</p>
            </div>
        </div>
    </div>


    <p v-else>Loading item details...</p>

</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';

interface AuctionItem {
    id: number;
    title: string;
    description: string;
    startingBid: number;
    currentBid: number;
    imageUrl: string | null;
    endDate: string;
}

export default defineComponent({
    name: 'AuctionItemDetail',
    setup() {
        const route = useRoute();
        const item = ref<AuctionItem | null>(null);
        const placeholderUrl = '/static/api/spa/assets/placeholder.jpg';

        const formatEndDate = (end: string) => {
            const endDate = new Date(end);
            return endDate.toLocaleString();
        };

        const fetchItemDetails = async (id: number) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/api/auction-items/${id}/`);
            if (!response.ok) {
                throw new Error('Failed to fetch item details');
            }
            const data = await response.json();

            // Map backend snake_case to frontend camelCase
            item.value = {
                id: data.id,
                title: data.title,
                description: data.description,
                startingBid: parseFloat(data.starting_bid),
                currentBid: data.current_bid ? parseFloat(data.current_bid) : 0,
                imageUrl: data.image,
                endDate: data.end_datetime
            };
        } catch (error) {
            console.error(error);
        }}

        onMounted(() => {
            const itemId = Number(route.params.id);
            if (!isNaN(itemId)) {
                fetchItemDetails(itemId);
            }
        });

        return {
            item,
            placeholderUrl,
            formatEndDate
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
</style>
