module.exports = function(config){
  config.set({

    basePath : './',

    files : [
      'app/bower_components/angular/angular.js',
      'app/bower_components/angular-route/angular-route.js',
      'app/bower_components/angular-mocks/angular-mocks.js',
      'app/bower_components/angular-animate/angular-animate.js',
      'app/bower_components/angular-aria/angular-aria.js',
      'app/bower_components/angular-material/angular-material.js',
      'app/bower_components/angular-material-icons/angular-material-icons.js',
      'app/bower_components/angular-messages/angular-messages.js', 
      'app/bower_components/angular-bootstrap/ui-bootstrap-tpls.js',
      'app/bower_components/ng-file-upload/ng-file-upload.js',
      "app/bower_components/ng-file-upload/ng-file-upload-shim.js",
      "app/bower_components/three.js/three.min.js", 
      'app/components/**/*.js',
      'app/app.js',
      'app/oga_facade/build-mocked-patients.js',
      'app/gait_analysis/**/*.js',
      'app/oga_facade*/**/*.js',
      'app/patient*/**/*.js'
    ],

    autoWatch : true,

    frameworks: ['jasmine'],

    browsers : ['Chrome'],

    plugins : [
            'karma-chrome-launcher',
            'karma-firefox-launcher',
            'karma-jasmine',
            'karma-junit-reporter'
            ],

    junitReporter : {
      outputFile: 'test_out/unit.xml',
      suite: 'unit'
    }

  });
};
