// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import NewAuctionItem from "../pages/NewAuctionItem.vue";
import AuctionItemDetail from "../pages/AuctionItemDetail.vue";
import AuctionItemList from "../pages/AuctionItemList.vue";

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Main Page', component: AuctionItemList },
        { path: '/new-auction-item/', name: 'New Auction Item', component: NewAuctionItem },
        { path: '/item/:id', name: 'AuctionItemDetail', component: AuctionItemDetail },
        { path: '/auction-items', name: 'AuctionItemList', component: AuctionItemList }
    ]
})

export default router
