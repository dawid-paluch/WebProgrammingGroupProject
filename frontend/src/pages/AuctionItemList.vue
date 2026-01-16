<template>

    <div class="auction-item-list">

        <h1>Auction Items</h1>

        <input
            type="text"
            v-model="searchQuery"
            placeholder="Search auction items..."
            class="search-bar"
            @input="debouncedFetch"
        />

        <div v-if="loading" class="loading">Loading auction items...</div>

        <p v-if="!loading && items.length === 0">No auction items found.</p>

        <div class="items-grid">
            <div
                v-for="item in items"
                :key="item.id"
                class="item-card"
                :class="{ 'ending-soon': new Date(item.endDate).getTime() - Date.now() < 24 * 60 * 60 * 1000 }"
                @click="goToItem(item.id)"
            >
                <img
                    :src="item.imageUrl ?? '/static/api/spa/assets/placeholder.jpg'"
                    alt="Item Image"
                />

                <h3>{{ item.title }}</h3>

                <p class="description">{{ item.description }}</p>

                <p class="price">
                    Current Bid: £{{ formatBid(item.currentBid, item.startingBid) }}
                </p>

                <p class="end-time">
                    {{ formatEndTime(item.endDate) }}
                </p>

            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuctionStore, AuctionItem } from '../stores/auctionStore';
import NewAuctionItem from './NewAuctionItem.vue';


const formatEndTime = (end: string) => {
    const endDate = new Date(end);
    const now = new Date();
    const diff = endDate.getTime() - now.getTime();

    if (diff <= 0) return 'Auction ended';

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((diff / (1000 * 60)) % 60);

    return `Ends in ${days}d ${hours}h ${minutes}m`;
};

export default defineComponent({
    name: 'AuctionItemList',
    setup() {
        const auctionStore = useAuctionStore();
        const items = computed(() => auctionStore.items);
        const searchQuery = ref('');
        const loading = ref(false);
        const router = useRouter();


        function debounce(func: (...args: any[]) => void, wait: number) {
            let timeout: number | undefined;
            return (...args: any[]) => {
                clearTimeout(timeout);
                timeout = window.setTimeout(() => {
                    func(...args);
                }, wait);
            };
        }

        const formatBid = (current: number, starting: number) => {
            return (current || starting).toFixed(2);
        };

        const fetchItemsDebounced = debounce(async () => {
            loading.value = true;
            await auctionStore.fetchItems(searchQuery.value);
            loading.value = false;
        }, 300);

        const goToItem = (itemId: number) => {
            router.push({ name: 'AuctionItemDetail', params: { id: itemId } });
        };

        onMounted(async () => {
            loading.value = true;
            await auctionStore.fetchItems();
            loading.value = false;
        });

        return {
            items,
            searchQuery,
            loading,
            goToItem,
            formatBid,
            formatEndTime,
            debouncedFetch: fetchItemsDebounced,
        };
    },
})

</script>

<style scoped>

.auction-item-list {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

.search-bar {
    width: 100%;
    padding: 10px;
    margin-bottom: 20px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.items-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
}

.item-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    cursor: pointer;
    transition: box-shadow 0.3s ease;
}

.item-card:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}

.item-card img {
    width: 100%;
    height: 150px;
    object-fit: cover;
    border-radius: 4px;
    margin-bottom: 10px;
}

.item-card .description {
    font-size: 14px;
    color: #555;
    margin-bottom: 10px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;  
    overflow: hidden;
}

.item-card .price {
    font-weight: bold;
    color: #1a73e8;
    margin-bottom: 5px;
}

.item-card .end-time {
    font-size: 12px;
    color: #888;
}

.loading {
    font-size: 18px;
    text-align: center;
    margin: 20px 0;
}

.item-card.ending-soon {
    border: 2px solid red;
}

</style>