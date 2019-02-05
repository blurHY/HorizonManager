import DashboardLayout from "@/layout/dashboard/DashboardLayout";
// GeneralViews
import NotFound from "@/pages/NotFoundPage";

// Admin pages
import Dashboard from "@/pages/Dashboard";
import LogPage from "@/pages/LogPage";
import Login from "@/pages/Login"

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
  },
  {
    path: "/login",
    name: "login",
    component: Login
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