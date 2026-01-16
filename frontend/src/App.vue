<template>
    <main class="container pt-4">
        <router-link v-if="$route.name !== 'Main Page'" :to="{name: 'Main Page'}" id="home-button">Home</router-link>
        
        <div id="account-menu">
            <!--<img
            :src="profileImageUrl"
            alt="Profile Picture button"
            class="profile-pic"
            @click="toggleMenu"
            />-->
            <button @click="toggleMenu" class="account-button">Account</button>

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
import { defineComponent, ref, onMounted } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
  components: { RouterView },

  setup() {
    const menuOpen = ref(false);
    const profileImageUrl = ref('/static/api/spa/assets/profile-placeholder.webp');

    // Toggle the dropdown menu
    const toggleMenu = () => {
      menuOpen.value = !menuOpen.value;
    };

    /*// Fetch current user profile image
    const fetchProfileImage = async () => {
      try {
        const res = await fetch('/api/profile/');
        if (!res.ok) throw new Error('Failed to fetch profile');
        const data = await res.json();
        if (data.profile_image) {
          profileImageUrl.value = data.profile_image.startsWith('/media/')
            ? data.profile_image
            : `/media/${data.profile_image}`;
        }
      } catch (err) {
        console.error(err);
      }
    };*/

    // Logout method
    const logout = async () => {
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
    };

    onMounted(() => {
      // fetchProfileImage();
    });

    return {
      menuOpen,
      profileImageUrl,
      toggleMenu,
      logout
    };
  }
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

.account-button {
    font-size: 1.2em;
    padding: 0.4em 1em;
    background-color: #555;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
</style>
