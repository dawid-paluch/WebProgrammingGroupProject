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
                @click="goToItem(item.id)"
            >
                <img
                    v-if="item.image"
                    :src="item.image"
                    alt="Item Image"
                />

                <h3>{{ item.title }}</h3>

                <p class="description">{{ item.description }}</p>

                <p class="price">
                    Current Bid: £{{ formatBid(item.current_bid, item.starting_bid) }}
                </p>

                <p class="end-time">
                Ends at: {{ new Date(item.end_datetime).toLocaleString() }}
                </p>
        
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

interface AuctionItem {
    id: number;
    title: string;
    description: string;
    image: string | null;
    starting_bid: string;
    current_bid: string | null;
    end_datetime: string;
}

export default defineComponent({
    name: 'AuctionItemList',
    setup() {
        const items = ref<AuctionItem[]>([]);
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

        const formatBid = (current: string | null, starting: string) => {
            const bid = current ?? starting; 
            return parseFloat(bid).toFixed(2);
        };

        const fetchAuctionItems = async () => {
            loading.value = true;
            try {
                const response = await fetch(
                    `http://127.0.0.1:8000/api/auction-items/?search=${encodeURIComponent(searchQuery.value)}`
                );

                if (!response.ok) throw new Error('Failed to fetch auction items');

                items.value = await response.json();
            } catch (error) {
                console.error('Error fetching auction items:', error);
            } finally {
                loading.value = false;
            }
        };

        const debouncedFetch = debounce(fetchAuctionItems, 300);

        const goToItem = (itemId: number) => {
            router.push({ name: 'AuctionItemDetail', params: { id: itemId } });
        };

        onMounted(() => {
            fetchAuctionItems();
        });

        return {
            items,
            searchQuery,
            loading,
            fetchAuctionItems,
            goToItem,
            debouncedFetch,
            formatBid,
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
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
}

.item-card .price {
    font-weight: bold;
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

</style>