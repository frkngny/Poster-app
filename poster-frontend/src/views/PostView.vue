<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <div class="main-center col-span-3 space-y-1">
            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-if="post.id" v-bind:key="post.id">
                <Post :post="this.post" />
                <form action="" method="post" v-on:submit.prevent="sendComment">
                    <div class="p-4">
                        <textarea v-model="commentBody" class="p-4 w-full bg-gray-100 rounded-lg"
                            placeholder="Comment..."></textarea>
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Comment</button>
                    </div>
                </form>
            </div>
            <hr>
            <div class="p-4 bg-white border border-gray-200 rounded-lg">
                <div class="p-4 bg-white border-b border-gray-200" v-for="comment in post_comments"
                    v-bind:key="comment.id">
                    <Comment :comment="comment" />
                </div>
            </div>
        </div>

    </div>
</template>
<script>
import axios from 'axios'
import Post from '../components/Post.vue'
import Comment from '../components/Comment.vue'

export default {
    name: 'PostDetail',
    components: {
        Post,
        Comment,
    },
    data() {
        return {
            interval: null,
            post: {},
            commentBody: '',
            post_comments: []
        }
    },
    created() {
        this.getPost()
        //this.getComments()
        //this.interval = setInterval(this.refreshPost, 5000)
    },
    beforeDestroy() {
        //clearInterval(this.interval)
    },
    methods: {
        getPost() {
            axios.get(`/api/posts/${this.$route.params.id}`)
                .then((response) => {
                    this.post = response.data
                    this.post_comments = response.data.post_comments
                })
                .catch((error) => {
                    console.log('error', error)
                })
        },
        sendComment() {
            axios.post(`/api/posts/${this.post.id}/comment`, { 'body': this.commentBody })
                .then((response) => {
                    if (response.status === 200) {
                        this.post = response.data.post
                        this.comment_count = response.data.post.comments_count
                        this.post_comments.unshift(response.data.comment)
                        this.commentBody = ''
                    } else {
                        console.log(response)
                    }
                })
                .catch((error) => {
                    console.log('error', error)
                })
        },
        getComments() {
            axios.get(`/api/posts/${this.$route.params.id}/comment`)
                .then((response) => {
                    this.comments = response.data
                })
                .catch((error) => {
                    console.log('error', error)
                })
        },
        refreshPost() {
            axios.get(`/api/posts/${this.post.id}`)
                .then((response) => {
                    this.like_count = response.data.likes_count
                })
                .catch((error) => {
                    console.log('error', error)
                })
        },
    }
}
</script>