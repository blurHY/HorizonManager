import DashboardLayout from "@/layout/dashboard/DashboardLayout.vue";
// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";

// Admin pages
import Dashboard from "@/pages/Dashboard.vue";
import LogPage from "@/pages/LogPage.vue"

const routes = [{
    path: "/",
    component: DashboardLayout,
    redirect: "/dashboard",
    children: [{
      path: "dashboard",
      name: "dashboard",
      component: Dashboard
    }, {
      path: "logfile",
      name: "logfile",
      component: LogPage
    }]
  },
  {
    path: "*",
    component: NotFound
  }
];

/**
 * Asynchronously load view (Webpack Lazy loading compatible)
 * The specified component must be inside the Views folder
 * @param  {string} name  the filename (basename) of the view to load.
function view(name) {
   var res= require('../components/Dashboard/Views/' + name + '.vue');
   return res;
};**/

export default routes;