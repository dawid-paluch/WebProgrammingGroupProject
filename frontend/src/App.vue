<template>
    <main class="container pt-4">
        <router-link v-if="$route.name !== 'Main Page'" :to="{name: 'Main Page'}" id="home-button">Home</router-link>
        <button id="logout-button" @click="logout">Log out</button>
        <!--<button id="new-item-button" @click="$router.push('/new-auction-item/')">New Item</button>-->
        <router-link v-if="$route.name !== 'New Auction Item'" :to="{ name: 'New Auction Item' }" id="new-item-button">New Item</router-link>

        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView },

    methods: {
        async logout() {
            const tokenEl = document.querySelector('meta[name="csrf-token"]') as HTMLMetaElement | null;
            const csrfToken = tokenEl?.content;
            
            if (!csrfToken) {
                console.error("CSRF token meta tag not found. Add <meta name=\"csrf-token\" content=\"{{ csrf_token }}\"> in the Django template.");
                return;
            }

            await fetch("/logout/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                },
                credentials: "same-origin",
            });
            
            window.location.href = "/login/";
        },
    },
});

</script>

<style scoped>
#logout-button {
    position: absolute;
    font-size: 1.2em;
    top: 1em;
    left: 1em;
    padding: 0.4em 1em;
    background-color: #ff4d4f;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

#new-item-button {
    position: absolute;
    font-size: 1.2em;
    top: 1em;
    right: 1em;
    padding: 0.4em 1em;
    background-color: #4dafff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

#home-button {
    position: absolute;
    font-size: 1.2em;
    top: 1em;
    left: 50%;
    transform: translateX(-50%);
    padding: 0.4em 1em;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

#home-button:hover{
    background-color: #3e8e41
}

</style>
