var promiseUnit = function (x) {
    var res = new $.Deferred();
    res.resolveWith(null, [x]);
    return res.promise();
}

var promiseBind = function (promise, continuation) {
    var res = new $.Deferred();
    promise.then(function (val1) {
        continuation(val1).then(function (val2) {
            res.resolveWith(val2);
        });
    });
    return res.promise();
}

var promisePipe = function (promise, continuations) {
    continuations.forEach(function (continuation) {
        promise = promiseBind(promise, continuation);
    });
    return promise;
}
