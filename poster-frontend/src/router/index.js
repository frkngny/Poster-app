import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import FeedView from '../views/FeedView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '@/views/ProfileView.vue'
import FriendsView from '@/views/FriendsView.vue'
import PostView from '@/views/PostView.vue'
import ChatView from '@/views/ChatView.vue'
import { useUserStore } from '@/stores/user'
import TrendView from '@/views/TrendView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView
        },
        {
            path: '/about',
            name: 'about',
            component: AboutView
        },
        {
            path: '/signup',
            name: 'signup',
            component: SignupView
        },
        {
            path: '/login',
            name: 'login',
            component: LoginView
        },
        {
            path: '/feed',
            name: 'feed',
            component: FeedView
        },
        {
            path: '/chat',
            name: 'chat',
            component: ChatView
        },
        {
            path: '/search',
            name: 'search',
            component: SearchView
        },
        {
            path: '/profile/:id',
            name: 'profile',
            component: ProfileView
        },
        {
            path: '/profile/:id/friends',
            name: 'friends',
            component: FriendsView
        },
        {
            path: '/post/:userid/:id',
            name: 'post',
            component: PostView
        },
        {
            path: '/trends/:tag',
            name: 'trendview',
            component: TrendView
        }
    ]
})

router.beforeEach(async (to) => {
    const publicPages = ['/login', '/signup', '/about']
    const authRequired = !publicPages.includes(to.path)
    const userStore = useUserStore()

    let navToLogin = false
    if (userStore.user) {
        if (!userStore.user.isAuthenticated){
            navToLogin = true
        }
    } else {
        navToLogin = true
    }

    if(authRequired && navToLogin){
        return '/login'
    }    
});

export default router
