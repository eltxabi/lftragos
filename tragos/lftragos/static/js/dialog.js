(function(angular) {
  'use strict';
angular.module('dialog', [])

.service('dialogService', DialogService);

function DialogService($q) {
  this.confirm = function(message) {
    return $q.when(window.confirm(message || 'Is it OK?'));
  };
}
})(window.angular);

/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/