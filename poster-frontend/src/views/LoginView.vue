<template>
    <title>Login</title>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Login</h1>

                <p class="mb-6 text-gray-500">
                    Welcome to Poster! <br>
                    A place where you post your thoughts as a poster.
                </p>

                <p class="font-bold">
                    <RouterLink :to="{ 'name': 'signup' }" class="underline">Don't have an account</RouterLink>?
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <div>
                        <label>E-mail</label><br>
                        <input type="email" v-model="form.email" placeholder="Your e-mail address"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Password</label><br>
                        <input type="password" v-model="form.password" placeholder="Your password"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Login</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
import { useUserStore } from "@/stores/user"
import { useToastStore } from '@/stores/toast';

export default {
    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore();
        return {
            userStore,
            toastStore
        }
    },
    data() {
        return {
            form: {
                email: '',
                password: '',
            },
            errors: []
        }
    },
    methods: {
        async submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Please enter your email address')
            }
            if (this.form.password === '') {
                this.errors.push('Please enter password')
            }

            if (this.errors.length === 0) {
                await axios.post('/api/login', this.form)
                    .then((response) => {
                        if (response.status === 200) {
                            this.userStore.setToken(response.data)

                            axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access
                        } else {
                            axios.defaults.headers.common["Authorization"] = ""
                            console.log(response)
                        }
                    })
                    .catch((error) => {
                        axios.defaults.headers.common["Authorization"] = ""
                        this.toastStore.showToast(3000, error.response.data.detail, 'bg-red-300')
                    })

                await axios.get('/api/me')
                    .then((response) => {
                        if (response.status === 200) {
                            this.userStore.setUserInfo(response.data)
                            this.$router.push('/feed')
                        } else {
                            console.log(response)
                        }
                    })
                    .catch((error) => {
                        this.toastStore.showToast(3000, error.response.data.detail, 'bg-red-300')
                    })
            }
        }
    }
}
</script>
