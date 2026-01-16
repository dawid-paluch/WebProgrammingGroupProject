<template>
    <main class="container pt-4">
        <router-link v-if="$route.name !== 'Main Page'" :to="{name: 'Main Page'}" id="home-button">Home</router-link>
        
        <div id="account-menu">
            <img
            :src="profileImageUrl"
            alt="Profile"
            id="profile-button"
            @click="toggleMenu"
            />

            <div v-if="menuOpen" id="account-dropdown">
                <router-link
                :to="{ name: 'Profile' }"
                class="dropdown-item"
                @click="menuOpen = false"
                >
                Edit Profile
                </router-link>

                <button class="dropdown-item" @click="logout">
                Log out
                </button>
            </div>
        </div>

        <router-link v-if="$route.name !== 'New Auction Item'" :to="{ name: 'New Auction Item' }" id="new-item-button">New Item</router-link>

        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView },

    data() {
        return {
            menuOpen: false,
            profileImageUrl: '/static/api/spa/assets/profile-placeholder.webp'
        };
    },

    methods: {
        toggleMenu() {
            this.menuOpen = !this.menuOpen;
        },

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

/*Profile dropdown menu style */

#account-menu {
    position: absolute;
    top: 1em;
    left: 1em;
}

#account-button {
    font-size: 1.2em;
    padding: 0.4em 1em;
    background-color: #555;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

#account-dropdown {
    margin-top: 0.3em;
    background: white;
    border-radius: 4px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    display: flex;
    flex-direction: column;
}

.dropdown-item {
    padding: 0.5em 1em;
    text-decoration: none;
    color: black;
    background: none;
    border: none;
    text-align: left;
    cursor: pointer;
}

.dropdown-item:hover {
    background-color: #eee;
}

#profile-button {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    cursor: pointer;
    object-fit: cover;
    border: 2px solid white;
}


</style>
