<template>
    <main class="container pt-4">
        <button @click="logout">Log out</button>

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
</style>
