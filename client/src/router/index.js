import Vue from 'vue';
import Router from 'vue-router';
import Show from '@/components/Show';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/show',
      name: 'Show',
      component: Show,
    },
  ],
  mode: 'history'
});
