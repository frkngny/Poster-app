<template>
    <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <h3 class="mb-6 text-xl">Trends</h3>

        <div class="space-y-4">
            <div class="flex items-center justify-between" v-for="trend in trends">
                <p class="text-xs">
                    <strong>{{ trend.tag }}</strong><br>
                    <span class="text-gray-500">{{ trend.count }} posts</span>
                </p>

                <RouterLink :to="{ name: 'trendview', params: { tag: trend.tag.replace('#', '') } }"
                    class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">Explore</RouterLink>
            </div>

        </div>
    </div>
</template>
<script>
import axios from 'axios';
import { RouterLink } from 'vue-router';

export default {
    name: 'trends',
    data() {
        return {
            trends: []
        }
    },
    mounted() {
        this.getTrends()
    },
    methods: {
        getTrends() {
            axios.get('/api/posts/trend_tags')
                .then(response => {
                    this.trends = response.data
                })
                .catch(error => {
                    console.log('error', error);
                })
        }
    }
}
</script>
<style lang="">

</style>