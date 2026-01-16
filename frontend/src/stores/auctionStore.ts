import { defineStore } from 'pinia';
import { ref } from 'vue';

function getCookie(name: string): string | null {
  const match = document.cookie.match(new RegExp("(^|; )" + name + "=([^;]*)"));
  return match ? decodeURIComponent(match[2]) : null;
}

export interface AuctionItem {
    id: number;
    title: string;
    description: string;
    startingBid: number;
    currentBid: number;
    imageUrl: string | null;
    endDate: string;
    ownerUsername: string;
}

export const useAuctionStore = defineStore('auctionStore', () => {
    const items = ref<AuctionItem[]>([]);

    function setItem(updatedItem: AuctionItem) {
        const index = items.value.findIndex(item => item.id === updatedItem.id);
        if (index >= 0) {
            items.value[index] = updatedItem;
        } else {
            items.value.push(updatedItem);
        }
    }

    function updateBid(itemId: number, bid: number) {
        const item = items.value.find(item => item.id === itemId);
        if (item) item.currentBid = bid;
    }

    function getItem(itemId: number) {
        return items.value.find(i => i.id === itemId) || null;
    }

    async function fetchItems(search = '') {
        try {
            const response = await fetch(
                `/api/auction-items/?search=${encodeURIComponent(search)}`
            );
            if (!response.ok) throw new Error('Failed to fetch auction items');
            const data = await response.json();

            // Convert backend data to AuctionItem[]
            items.value = data.map((d: any) => ({
                id: d.id,
                title: d.title,
                description: d.description,
                startingBid: parseFloat(d.starting_bid),
                currentBid: d.current_bid ? parseFloat(d.current_bid) : parseFloat(d.starting_bid),
                imageUrl: d.image,
                endDate: d.end_datetime,
            }));
        } catch (err) {
            console.error(err);
        }
    }

    async function createItem(newItem: {
        title: string;
        description: string;
        startingBid: number;
        endDate: string;
        imageFile?: File | null;
    }) {
        const formData = new FormData();
        formData.append('title', newItem.title);
        formData.append('description', newItem.description);
        formData.append('starting_bid', newItem.startingBid.toFixed(2));
        formData.append('end_datetime', newItem.endDate);
        if (newItem.imageFile) formData.append('image', newItem.imageFile);

        const csrfToken = getCookie('csrftoken');

        const response = await fetch(`/api/auction-items/`, {
            method: 'POST',
            body: formData,
            credentials: 'same-origin',
            headers: csrfToken ? { 'X-CSRFToken': csrfToken } : {},
        });

        if (!response.ok) {
            const text = await response.text();
            try {
                const data = JSON.parse(text);
                throw new Error(
                    Object.values(data)
                        .map((v: any) => (Array.isArray(v) ? v.join(', ') : v))
                        .join(', ')
                );
            } catch {
                throw new Error(text || `Request failed with status ${response.status}`);
            }
        }

        const created = await response.json();

        // Add to local state
        setItem({
            id: created.id,
            title: created.title,
            description: created.description,
            startingBid: parseFloat(created.starting_bid),
            currentBid: created.current_bid ? parseFloat(created.current_bid) : 0,
            imageUrl: created.image,
            endDate: created.end_datetime,
            ownerUsername: created.ownerUsername
        });

        return created;
    }

    return { items, setItem, updateBid, getItem, fetchItems, createItem };
});
