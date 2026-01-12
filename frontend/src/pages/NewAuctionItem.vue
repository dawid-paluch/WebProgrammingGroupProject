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
        <input type="number" id="startingBid" v-model="startingBid" required />
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

export default defineComponent({
    name: 'NewAuctionItem',
    setup() {
        const title = ref('');
        const description = ref('');
        const startingBid = ref(0);
        const endDate = ref('');
        const imageFile = ref(null);
        const errorMessage = ref('');
        const router = useRouter();


        const handleFileUpload = (event : Event) => {
            const target = event.target as HTMLInputElement;
            if (target.files && target.files.length > 0) {
                imageFile.value = target.files[0];
            }
        };

        const submitForm = async () => {
        console.log('submitForm called', endDate.value);

        const formData = new FormData();
        formData.append('owner', 'test_user');
        formData.append('title', title.value.trim());
        formData.append('description', description.value.trim());
        formData.append('starting_bid', Number(startingBid.value).toFixed(2));

        if (endDate.value) {
            const formattedEndDate = endDate.value.length === 16 
                ? endDate.value + ':00' 
                : endDate.value;
            console.log('Sending end_datetime (local format):', formattedEndDate);
            formData.append('end_datetime', formattedEndDate);
        }

        if (imageFile.value) {
            formData.append('image', imageFile.value);
        }

        // log all formData entries
        for (const [key, value] of (formData as any).entries()) {
            console.log('FormData:', key, value);
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/api/auction-items/', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const text = await response.text();
                console.log('Raw response from backend:', text);

                try {
                    const data = JSON.parse(text);
                    console.log('Parsed JSON backend errors:', data);
                    errorMessage.value = Object.values(data)
                        .map(v => Array.isArray(v) ? v.join(', ') : v)
                        .join(', ');
                } catch {
                    errorMessage.value = text || `Request failed with status ${response.status}`;
                }
                return;
            }

            const createdItem = await response.json();
            router.push(`/items/${createdItem.id}`);
        } catch (error) {
            errorMessage.value = (error as Error).message;
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