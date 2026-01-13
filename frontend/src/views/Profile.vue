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
    <div>
        <h1>Profile</h1>

        <label for="">Email</label>
        <input v-model="email" type="email" />

        <label for="">Date of Birth</label>
        <input v-model="dateOfBirth" type="date" />

        <label for="">Profile Image</label>
        <input type="file" @change="onFileChange" />

        <button @click="saveProfile">Save</button>
    </div>
</template>