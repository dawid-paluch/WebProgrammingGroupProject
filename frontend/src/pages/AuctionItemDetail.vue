<template>

    <div class="auction-item-detail" v-if="item">

        <h1>{{ item.title }}</h1>
        <img v-if= "item.imageUrl" :src="item.imageUrl" alt="Auction Item Image" style="max-width: 400px" />
        <p><strong>Description:</strong> {{ item.description }}</p>
        <p><strong>Starting Bid:</strong> ${{ item.startingBid.toFixed(2) }}</p>
        <p><strong>Current Bid:</strong> ${{ item.currentBid.toFixed(2) }}</p>
        <p><strong>Auction End Date:</strong> {{ new Date(item.endDate).toLocaleString() }}</p>
   
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
        }};

        onMounted(() => {
            const itemId = Number(route.params.id);
            if (!isNaN(itemId)) {
                fetchItemDetails(itemId);
            }
        });

        return {
            item
        };
    }
});

</script>

<style scoped>
.auction-item-detail img {
    display: block;
    margin-bottom: 20px;
}

</style>