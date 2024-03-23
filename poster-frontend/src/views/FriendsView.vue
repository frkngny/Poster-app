<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-center col-span-3 space-y-4">

            <div class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-4 gap-4" v-if="friends.length">
                <div class="p-4 text-center bg-gray-100 rounded-lg" v-for="friend in friends">
                    <RouterLink :to="{ 'name': 'profile', params: { 'id': friend.id } }">
                        <img src="https://i.pravatar.cc/100?img=70" class="mb-6 mx-auto rounded-full">

                        <p><strong>{{ friend.name }}</strong></p>
                    </RouterLink>

                    <div class="mt-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">{{ friend.get_friends_count }} friends</p>
                        <p class="text-xs text-gray-500">{{ friend.get_posts_count }} posts</p>
                    </div>
                </div>
            </div>

            <div class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-4 gap-4"
                v-if="received_requests.length && this.userStore.user.id === this.user.id">
                <div class="p-4 text-center bg-gray-100 rounded-lg" v-for="req in received_requests" v-bind:key="req.sender.name">
                    <RouterLink :to="{ 'name': 'profile', params: { 'id': req.sender.id } }">
                        <img src="https://i.pravatar.cc/100?img=70" class="mb-6 mx-auto rounded-full">

                        <p><strong>{{ req.sender.name }}</strong></p>
                    </RouterLink>

                    <div class="mt-6 space-x-4">
                        <button class="inline-block py-2 px-2 bg-purple-600 text-white rounded-lg" @click="handleRequest('accepted', req.sender.id)">Accept</button>
                        <button class="inline-block py-2 px-2 bg-red-600 text-white rounded-lg" @click="handleRequest('rejected', req.sender.id)">Reject</button>
                    </div>
                </div>
            </div>

            <div class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-5 gap-4"
                v-if="sent_requests.length && this.userStore.user.id === this.user.id">
                <div class="p-4 text-center bg-gray-100 rounded-lg" v-for="req in sent_requests" v-bind:key="req.receiver.name">
                    <RouterLink :to="{ 'name': 'profile', params: { 'id': req.receiver.id } }">
                        <img src="https://i.pravatar.cc/100?img=70" class="mb-6 mx-auto rounded-full">

                        <p><strong>{{ req.receiver.name }}</strong></p>
                    </RouterLink>

                    <div class="mt-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">Request is sent</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />
        </div>

    </div>
</template>
<script>
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import axios from 'axios'
import { useUserStore } from "@/stores/user"


export default {
    name: 'FriendsView',
    setup() {
        const userStore = useUserStore()
        return {
            userStore
        }
    },
    components: {
        PeopleYouMayKnow,
    },
    data() {
        return {
            user: {},
            friends: [],
            received_requests: [],
            sent_requests: [],
        }
    },
    mounted() {
        this.getFriends()
        this.getRequests()
    },
    methods: {
        getFriends() {
            axios.get(`/api/user/${this.$route.params.id}/friends`)
                .then((response) => {
                    this.friends = response.data.friends
                    this.user = response.data.user
                })
                .catch((error) => {
                    console.log('error', error)
                })
        },
        getRequests() {
            axios.get(`/api/user/${this.userStore.user.id}/friends/request`)
                .then((response) => {
                    this.received_requests = response.data.received_requests
                    this.sent_requests = response.data.sent_requests
                })
                .catch((error) => {
                    console.log('error', error)
                })
        },
        handleRequest(status, sender_id) {
            axios.put(`/api/user/${this.userStore.user.id}/friends/request`, { 'sender_id': sender_id, 'status': status })
                .then((response) => {
                    console.log(response.data)
                })
                .catch((error) => {
                    console.log(error);
                })
        }
    },

}
</script>