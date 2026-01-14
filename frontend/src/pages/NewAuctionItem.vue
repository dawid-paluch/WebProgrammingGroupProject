<template>
  <div class="new-auction-item">
    <h1>Create New Auction Item</h1>

    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="title">Title:</label>
        <input type="text" id="title" v-model="title" required />
      </div>

      <div class="form-group">
        <label for="description">Description:</label>
        <textarea id="description" v-model="description" required></textarea>
      </div>

      <div class="form-group">
        <label for="startingBid">Starting Bid:</label>
        <input type="number" id="startingBid" v-model="startingBid" step="0.01" min="0" placeholder="0.00" />
      </div>

      <div class="form-group">
        <label for="endDate">End Date:</label>
        <input type="datetime-local" id="endDate" v-model="endDate" required />
      </div>

      <div class="form-group">
        <label for="image">Image:</label>
        <input type="file" id="image" @change="handleFileUpload" />
      </div>

      <button type="submit" class="submit-btn">Create Auction Item</button>
    </form>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuctionStore } from '../stores/auctionStore';   

export default defineComponent({
    name: 'NewAuctionItem',
    setup() {
        const auctionStore = useAuctionStore();
        const router = useRouter();

        const title = ref('');
        const description = ref('');
        const startingBid = ref(0);
        const endDate = ref('');
        const imageFile = ref<File | null>(null);
        const errorMessage = ref('');


        const handleFileUpload = (event : Event) => {
            const target = event.target as HTMLInputElement;
            if (target.files && target.files.length > 0) {
                imageFile.value = target.files[0];
            }
        };

        const submitForm = async () => {
            errorMessage.value = '';

            if (!title.value || !description.value || !endDate.value) {
                errorMessage.value = 'Please fill in all required fields.';
                return;
            }

            try {
                // call the Pinia store method
                const createdItem = await auctionStore.createItem({
                title: title.value.trim(),
                description: description.value.trim(),
                startingBid: Number(startingBid.value),
                endDate: endDate.value.length === 16 ? endDate.value + ':00' : endDate.value,
                imageFile: imageFile.value,
                });

                // navigate to the newly created item's page
                router.push(`/item/${createdItem.id}`);
            } catch (error: any) {
                errorMessage.value = error.message || 'Failed to create auction item.';
            }
            };

        return {
            title,
            description,
            startingBid,
            endDate,
            imageFile,
            handleFileUpload,
            submitForm,
            errorMessage,
            
        };
    },
});
</script>

<style scoped>
.new-auction-item {
    max-width: 600px;
    margin: 40px auto;
    padding: 30px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #fff;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 1);
    font-family: Arial , sans-serif;
}

h1 {
    text-align: center;
    margin-bottom: 30px;
    font-size: 28px
}

.form-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
}

label {
    margin-bottom: 5px;
    font-weight: bold;
    color: #333;
}

input[type="text"],
input[type="number"],
input[type="datetime-local"],
textarea,
input[type="file"] {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 15px;
}

textarea {
    resize: vertical;
    min-height: 100px;
}

.submit-btn {
    width: 100%;
    padding: 12px;
    background-color: #1a73e8;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.2s ease, transform 0.1s ease;
}

.submit-btn:hover {
    background-color: #1669c1;
    transform: translateY(-2px);
}

.error {
    color: red;
    margin-top: 15px;
    text-align: center;
}

</style>