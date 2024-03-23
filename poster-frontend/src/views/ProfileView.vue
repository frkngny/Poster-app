<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">
                <p><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <RouterLink class="text-xs text-gray-500" :to="{ 'name': 'friends', params: { 'id': user.id } }">
                        {{ user.get_friends_count }} Friends
                    </RouterLink>
                    <p class="text-xs text-gray-500">{{ user.get_posts_count }} posts</p>
                </div>
                <div class="mt-6" v-if="user.id !== userStore.user.id">
                    <div class="mt-6 space-x-4" v-if="hasRequest">
                        <button class="inline-block py-2 px-2 bg-purple-600 text-white rounded-lg"
                            @click="handleIfRequest('accepted', user.id)">Accept</button>
                        <button class="inline-block py-2 px-2 bg-red-600 text-white rounded-lg"
                            @click="handleIfRequest('rejected', user.id)">Reject</button>
                    </div>
                    <p v-else-if="!hasRequest && hasBackRequest" class="text-xs text-gray-500">Pending friend request.
                    </p>
                    <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg"
                        @click="sendFriendRequest" v-else-if="!hasRequest && !hasBackRequest && myFriends.filter(usr => usr.id === user.id).length == 0">Add friend</button>
                </div>
            </div>
        </div>

        <div class="main-center col-span-2 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg" v-if="this.$route.params.id === userStore.user.id">
                <form action="" method="post" v-on:submit.prevent="submitForm">
                    <div class="p-4">
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
                            placeholder="What are you thinking about?"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <a href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach image</a>

                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                    </div>
                </form>
            </div>

            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-if="posts.length" v-for="post in posts"
                v-bind:key="post.id">
                <Post :post="post" />
            </div>
            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-else>
                <h2>Nothing to be shown here.</h2>
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />

            <Trends />
        </div>
    </div>
</template>
<script>
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import Post from '../components/Post.vue'
import axios from 'axios'
import { useUserStore } from "@/stores/user"
import { useToastStore } from '@/stores/toast';

export default {
    name: 'ProfileView',
    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()
        return {
            userStore,
            toastStore
        }
    },
    components: {
        PeopleYouMayKnow,
        Trends,
        Post,
    },
    data() {
        return {
            posts: [],
            body: '',
            user: {},
            my_received_requests: [],
            my_sent_requests: [],
            hasRequest: false,
            hasBackRequest: false,
            myFriends: []
        }
    },
    mounted() {
        this.getFeed()
        this.getProfile()
        this.getMyRequests()
        this.getMyFriends()
    },
    methods: {
        getFeed() {
            axios.get(`/api/posts/profile/${this.$route.params.id}`)
                .then((response) => {
                    this.posts = response.data
                })
                .catch((error) => {
                    console.log('error', error)
                })
        },
        submitForm() {
            axios.post('/api/posts/create', { 'body': this.body })
                .then((response) => {
                    this.posts.unshift(response.data)
                    this.body = ''
                })
                .catch((error) => {
                    console.log('error', error)
                })
        },
        getProfile() {
            axios.get(`/api/user/${this.$route.params.id}`)
                .then((response) => {
                    if (response.status === 200) {
                        this.user = response.data
                    }
                })
                .catch((error) => {
                    console.log('error', error)
                })
        },
        sendFriendRequest() {
            axios.post(`/api/user/${this.userStore.user.id}/friends/request`, { 'receiver': this.$route.params.id })
                .then((response) => {
                    if (response.status === 200) {
                        this.toastStore.showToast(3000, response.data.message, 'bg-emerald-300')
                    }
                })
                .catch((error) => {
                    if (error.response.status === 406) {
                        this.toastStore.showToast(3000, error.response.data.message, 'bg-red-300')
                    }
                })
        },
        getMyRequests() {
            axios.get(`/api/user/${this.userStore.user.id}/friends/request`)
                .then((response) => {
                    for (let index = 0; index < response.data.received_requests.length; index++) {
                        if (response.data.received_requests[index].sender.id === this.user.id)
                            this.hasRequest = true;
                    }
                    for (let index = 0; index < response.data.sent_requests.length; index++) {
                        if (response.data.sent_requests[index].receiver.id === this.user.id)
                            this.hasBackRequest = true;
                    }
                    this.my_received_requests = response.data.received_requests
                    this.my_sent_requests = response.data.sent_requests
                })
                .catch((error) => {
                    console.log('error', error)
                })
        },
        handleIfRequest(status, sender_id) {
            axios.put(`/api/user/${this.userStore.user.id}/friends/request`, { 'sender_id': sender_id, 'status': status })
                .then((response) => {
                    console.log(response.data)
                })
                .catch((error) => {
                    console.log(error);
                })
        },
        getMyFriends() {
            axios.get(`/api/user/${this.userStore.user.id}/friends`)
                .then((response) => {
                    this.myFriends = response.data.friends
                    console.log(this.myFriends);
                    console.log(this.user);
                })
                .catch((error) => {
                    console.log('error', error)
                })
        },
    },
    watch: {
        "$route.params.id": {
            handler() {
                this.getFeed()
                this.getProfile()
            },
            immediate: true,
            deep: true
        }
    }
}
</script>
<style lang="">

</style>