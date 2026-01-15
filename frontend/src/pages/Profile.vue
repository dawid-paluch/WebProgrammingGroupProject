<script lang="ts" setup>
import { onMounted, ref } from 'vue';


interface UserProfile {
  username: string;
  email: string;
  date_of_birth: string | null;
  profile_image: string | null;
}

const profile = ref<UserProfile | null>(null);
const email = ref("");
const dateOfBirth = ref("");
const profileImage = ref<File | null>(null);

function getCSRFToken(): string {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1] || '';
}

onMounted(async () => {
    const res = await fetch("api/profile/");
    const data = await res.json();
    profile.value = data;
    email.value = data?.email ?? "";
    dateOfBirth.value = data?.date_of_birth ?? "";
});

async function saveProfile() {
    const formData = new FormData();
    formData.append("email", email.value);
    if (dateOfBirth.value) {
        formData.append("date_of_birth", dateOfBirth.value);
    }
    if (profileImage.value) {
        formData.append("profile_image", profileImage.value);
    }

    await fetch("api/profile/", {
        method: "PUT",
        headers: {
            "X-CSRFToken": getCSRFToken(),
        },
        body: formData,
    });

    alert("Profile updated successfully!");
}

function onFileChange(e: Event) {
    const target = e.target as HTMLInputElement | null;
    const file = target?.files?.[0] ?? null;
    profileImage.value = file;
}
</script>

<template>
    <div class="profile-container">
        <h1>Profile</h1>
        <p>Edit your details below.</p>

        <label for="">Email</label>
        <input v-model="email" type="email" />

        <label for="">Date of Birth</label>
        <input v-model="dateOfBirth" type="date" />

        <label for="">Profile Image</label>
        <input type="file" @change="onFileChange" />

        <button @click="saveProfile">Save</button>
    </div>
</template>

<style>

.profile-container {
    max-width: 90%;
    margin: 3rem auto;
    padding: 2rem;
    border-radius: 12px;
    background-color: #f9f9f9;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.profile-container h1 {
    margin-bottom: 0.2rem;
    font-size: 2.5rem;
    color: #333;
}

.profile-container p {
    margin-bottom: 2rem;
    color: #666;
    font-size: 1.1rem;
}

.profile-container label {
    display: block;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    font-weight: bold;
    color: #555;
}

.profile-container input[type="email"],
.profile-container input[type="date"],
.profile-container input[type="file"] {
    width: 100%;
    padding: 0.5rem;
    border-radius: 8px;
    border: 1px solid #ccc;
    font-size: 1rem;
}

.profile-container button {
    margin-top: 2rem;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 8px;
    background-color: #4CAF50;
    color: white;
    font-size: 1.1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
.profile-container button:hover {
    background-color: #2b732e;
}
</style>