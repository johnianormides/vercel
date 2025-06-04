// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import AdminLogin from '../views/admin-login.vue';
import AddPet from '../views/admin/AddPet.vue';
import Applications from '../views/admin/Applications.vue';
import Dashboard from '../views/admin/Dashboard.vue';
import EditPet from '../views/admin/EditPet.vue';
import PetHistory from '../views/admin/PetHistory.vue';
import Pets from '../views/admin/Pets.vue';
import ViewPet from '../views/admin/ViewPet.vue';
import ConfirmEmail from '../views/confirm-email.vue';
import donations from '../views/donations.vue';
import HomeVue from '../views/home.vue';
import Login from '../views/login.vue';
import PetProfile from '../views/pet-profile.vue';
import PetProfiles from '../views/pet-profiles.vue';
import Signup from '../views/signup.vue';
import status from '../views/status.vue';
import stories from '../views/stories.vue';
import training from '../views/training.vue';

const routes = [
  {
    path: '/home',
    name: 'home',
    component: HomeVue
  },
  {
    path: '/pet-profile',
    name: 'petProfile',
    component: PetProfile
  },
  {
    path: '/pet-profile/:id',
    name: 'petProfileWithId',
    component: PetProfile,
    props: true
  },
  {
    path: '/donations',
    name: 'donations',
    component: donations
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/signup',
    name: 'signup',
    component: Signup
  },
  {
    path: '/admin',
    name: 'admin',
    component: Dashboard
  },
  {
    path: '/admin/dashboard',
    name: 'adminDashboard',
    component: Dashboard
  },
  {
    path: '/admin/pets',
    name: 'adminPets',
    component: Pets
  },
  {
    path: '/admin/pets/add',
    name: 'adminAddPet',
    component: AddPet
  },
  {
    path: '/admin/pets/view/:id',
    name: 'adminViewPet',
    component: ViewPet,
    props: true
  },
  {
    path: '/admin/pets/edit/:id',
    name: 'adminEditPet',
    component: EditPet,
    props: true
  },
  {
    path: '/admin/applications',
    name: 'adminApplications',
    component: Applications
  },
  {
    path: '/admin/pet-history',
    name: 'adminPetHistory',
    component: PetHistory
  },
  {
    path: '/pet-profiles',
    name: 'petProfiles',
    component: PetProfiles
  },
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/training',
    name: 'training',
    component: training
  },
  {
    path: '/stories',
    name: 'stories',
    component: stories
  },
  {
    path: '/status',
    name: 'status',
    component: status
  },
  {
    path: '/admin-login',
    name: 'adminLogin',
    component: AdminLogin
  },
  {
    path: '/confirm-email',
    name: 'confirmEmail',
    component: ConfirmEmail
  },
  // Ensure these route definitions are added to your routes array
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: () => import('../views/forgot-password.vue')
  },
  {
    path: '/reset-password',
    name: 'reset-password',
    component: () => import('../views/reset-password.vue')
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
