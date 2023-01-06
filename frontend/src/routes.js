import Home from './views/Home.vue'
import About from './views/About.vue'
import NotFound from './views/NotFound.vue'
import Form from './views/FormInput.vue'
import DisplayCit from './views/DisplayCitadel.vue'

/** @type {import('vue-router').RouterOptions['routes']} */
export const routes = [
  {
    path: '/about',
    meta: { title: 'About' },
    component: About,
    // example of route level code-splitting
    // this generates a separate chunk (About.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    // component: () => import('./views/About.vue')
  },
  { path: '/', component: Form, meta: { title: 'Form'}},
  { path: '/citadel', component: DisplayCit},
  { path: '/:path(.*)', component: NotFound },
]
