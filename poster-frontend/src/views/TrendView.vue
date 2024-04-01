<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <div class="main-center col-span-3 space-y-4">
            <div class="p-4 bg-white border border-gray-200">
                <h2 class="text-xl">Trend: <strong>#{{ this.$route.params.tag }}</strong></h2>
            </div>
            <div class="p-4 bg-gray-800 text-white border border-gray-200 rounded-lg" v-for="post in posts" v-bind:key="post.id">
                <Post :post="post"/> 
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

export default {
    name: 'TrendView',
    components: {
        PeopleYouMayKnow,
        Trends,
        Post,
    },
    data() {
        return {
            posts: [],
            body: '',
        }
    },
    mounted() {
        this.getFeed()
    },
    methods: {
        getFeed() {
            axios.get(`/api/posts/?in_friends=false&trend=${this.$route.params.tag}`)
                .then((response) => {
                    this.posts = response.data
                })
                .catch((error) => {
                    console.log('error', error)
                })
        },
    },
    watch: {
        "$route.params.tag": {
            handler() {
                this.getFeed()
            },
            immediate: true,
            deep: true
        }
    }
}
</script>
<style lang="">
    
</style>