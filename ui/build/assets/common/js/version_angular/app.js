'use strict';

angular.module('cleanUI', [
    'ngRoute',
    'cleanUI.controllers'
])
.config(['$locationProvider', '$routeProvider',
    function($locationProvider, $routeProvider) {

        /////////////////////////////////////////////////////////////
        // SYSTEM
        $routeProvider.when('/', {redirectTo: '/dashboards/alpha'});
        $routeProvider.otherwise({redirectTo: 'pages/page-404'});

        /////////////////////////////////////////////////////////////
        // Documentation
        $routeProvider.when('/documentation/index', {
            templateUrl: 'documentation/index.html'
        });

        /////////////////////////////////////////////////////////////
        // Dashboards
        $routeProvider.when('/dashboards/alpha', {
            templateUrl: 'dashboards/alpha.html'
        });

        $routeProvider.when('/dashboards/beta', {
            templateUrl: 'dashboards/beta.html'
        });

        /////////////////////////////////////////////////////////////
        // Apps
        $routeProvider.when('/apps/profile', {
            templateUrl: 'apps/profile.html'
        });

        $routeProvider.when('/apps/messaging', {
            templateUrl: 'apps/messaging.html'
        });

        $routeProvider.when('/apps/mail', {
            templateUrl: 'apps/mail.html'
        });

        $routeProvider.when('/apps/calendar', {
            templateUrl: 'apps/calendar.html'
        });

        $routeProvider.when('/apps/gallery', {
            templateUrl: 'apps/gallery.html'
        });

        /////////////////////////////////////////////////////////////
        // Layout
        $routeProvider.when('/layout/grid', {
            templateUrl: 'layout/grid.html'
        });

        $routeProvider.when('/layout/panels', {
            templateUrl: 'layout/panels.html'
        });

        $routeProvider.when('/layout/sidebars', {
            templateUrl: 'layout/sidebars.html'
        });

        $routeProvider.when('/layout/utilities', {
            templateUrl: 'layout/utilities.html'
        });

        $routeProvider.when('/layout/typography', {
            templateUrl: 'layout/typography.html'
        });

        /////////////////////////////////////////////////////////////
        // Icons
        $routeProvider.when('/icons/fontawesome', {
            templateUrl: 'icons/fontawesome.html'
        });

        $routeProvider.when('/icons/icomoon-ultimate', {
            templateUrl: 'icons/icomoon-ultimate.html'
        });

        /////////////////////////////////////////////////////////////
        // Forms
        $routeProvider.when('/forms/autocomplete', {
            templateUrl: 'forms/autocomplete.html'
        });

        $routeProvider.when('/forms/basic-form-elements', {
            templateUrl: 'forms/basic-form-elements.html'
        });

        $routeProvider.when('/forms/buttons', {
            templateUrl: 'forms/buttons.html'
        });

        $routeProvider.when('/forms/checkboxes-radio', {
            templateUrl: 'forms/checkboxes-radio.html'
        });

        $routeProvider.when('/forms/dropdowns', {
            templateUrl: 'forms/dropdowns.html'
        });

        $routeProvider.when('/forms/extras', {
            templateUrl: 'forms/extras.html'
        });

        $routeProvider.when('/forms/form-validation', {
            templateUrl: 'forms/form-validation.html'
        });

        $routeProvider.when('/forms/input-mask', {
            templateUrl: 'forms/input-mask.html'
        });

        $routeProvider.when('/forms/selectboxes', {
            templateUrl: 'forms/selectboxes.html'
        });


        /////////////////////////////////////////////////////////////
        // Components
        $routeProvider.when('/components/badges-labels', {
            templateUrl: 'components/badges-labels.html'
        });

        $routeProvider.when('/components/calendar', {
            templateUrl: 'components/calendar.html'
        });

        $routeProvider.when('/components/carousel', {
            templateUrl: 'components/carousel.html'
        });

        $routeProvider.when('/components/collapse', {
            templateUrl: 'components/collapse.html'
        });

        $routeProvider.when('/components/date-picker', {
            templateUrl: 'components/date-picker.html'
        });

        $routeProvider.when('/components/media-players', {
            templateUrl: 'components/media-players.html'
        });

        $routeProvider.when('/components/modal', {
            templateUrl: 'components/modal.html'
        });

        $routeProvider.when('/components/nestable', {
            templateUrl: 'components/nestable.html'
        });

        $routeProvider.when('/components/notifications-alerts', {
            templateUrl: 'components/notifications-alerts.html'
        });

        $routeProvider.when('/components/pagination', {
            templateUrl: 'components/pagination.html'
        });

        $routeProvider.when('/components/progress-bars', {
            templateUrl: 'components/progress-bars.html'
        });

        $routeProvider.when('/components/slider', {
            templateUrl: 'components/slider.html'
        });

        $routeProvider.when('/components/steps', {
            templateUrl: 'components/steps.html'
        });

        $routeProvider.when('/components/tabs', {
            templateUrl: 'components/tabs.html'
        });

        $routeProvider.when('/components/text-editor', {
            templateUrl: 'components/text-editor.html'
        });

        $routeProvider.when('/components/tooltips-popovers', {
            templateUrl: 'components/tooltips-popovers.html'
        });

        /////////////////////////////////////////////////////////////
        // Tables
        $routeProvider.when('/tables/basic-tables', {
            templateUrl: 'tables/basic-tables.html'
        });

        $routeProvider.when('/tables/datatables', {
            templateUrl: 'tables/datatables.html'
        });

        $routeProvider.when('/tables/editable-tables', {
            templateUrl: 'tables/editable-tables.html'
        });

        /////////////////////////////////////////////////////////////
        // Charts
        $routeProvider.when('/charts/c3', {
            templateUrl: 'charts/c3.html'
        });

        $routeProvider.when('/charts/chartistjs', {
            templateUrl: 'charts/chartistjs.html'
        });

        $routeProvider.when('/charts/peity', {
            templateUrl: 'charts/peity.html'
        });


        /////////////////////////////////////////////////////////////
        // Pages
        $routeProvider.when('/pages/invoice', {
            templateUrl: 'pages/invoice.html'
        });

        $routeProvider.when('/pages/lockscreen', {
            templateUrl: 'pages/lockscreen.html',
            controller: 'lockscreenPageCtrl'
        });

        $routeProvider.when('/pages/login', {
            templateUrl: 'pages/login.html',
            controller: 'loginPageCtrl'
        });

        $routeProvider.when('/pages/page-404', {
            templateUrl: 'pages/page-404.html'
        });

        $routeProvider.when('/pages/page-500', {
            templateUrl: 'pages/page-500.html'
        });

        $routeProvider.when('/pages/pricing-tables', {
            templateUrl: 'pages/pricing-tables.html'
        });

        $routeProvider.when('/pages/register', {
            templateUrl: 'pages/register.html',
            controller: 'registerPageCtrl'
        });

    }
]);

var app = angular.module('cleanUI.controllers', []);

app.controller('MainCtrl', function($location, $scope, $rootScope) {

    $scope.$on('$routeChangeSuccess', function() {

        // Set to default (show) state left and top menu, remove single page classes
        $('body').removeClass('single-page single-page-inverse');
        $rootScope.hideLeftMenu = false;
        $rootScope.hideTopMenu = false;

        // Firefox issue: scroll top when page load
        $('html, body').scrollTop(0);

        // Set active state menu after success change route
        $('.left-menu-list-active').removeClass('left-menu-list-active');
        $('nav.left-menu .left-menu-list-root .left-menu-link').each(function(){
            if ($(this).attr('href') == '#' + $location.path()) {
                $(this).closest('.left-menu-list-root > li').addClass('left-menu-list-active');
            }
        });

    });

});

app.directive('leftMenu', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            element.on('click', '.left-menu-link', function() {

                if (!$(this).closest('.left-menu-list-submenu').length) {
                    $('.left-menu-list-opened > a + ul').slideUp(200, function(){
                        $('.left-menu-list-opened').removeClass('left-menu-list-opened');
                    });
                }

            });
        }
    };
});