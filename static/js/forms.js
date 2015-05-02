var Form = function (selector) {
    this.$el = $(selector);
    var valToCheckedProp = function ($checkboxEl) {
        $checkboxEl.val($checkboxEl.prop('checked'));
    }
    var $checkboxes = this.$el.find('input[type=checkbox]');
    $checkboxes.each(function (index, el) {
        valToCheckedProp($(el));
    });
    $checkboxes.click(function (el) {
        valToCheckedProp($(this));
    });
}

Form.prototype = {

    getJson: function () {
        var jsonObj = {};
        var formData = this.$el.serializeArray();
        formData.forEach(function (input) {
            jsonObj[input.name] = input.value;
        });
        return jsonObj;
    },

    getJsonString: function () {
        return JSON.stringify(this.getJson());
    },

    showErrors: function (errDict) {
        this.$el.find('.help-block').remove();
        this.$el.find('.alert').remove();
        this.$el.find('input,textarea,select').each(function (index, el) {
            var $el = $(el);
            if ($el.attr('name') in errDict) {
                $el.parent().addClass('has-error');
                var $help = $('<p>');
                $help.addClass('help-block');
                $help.text(errDict[$el.attr('name')]);
                $help.insertAfter($el);
            } else {
                $el.parent().removeClass('has-error');
            }
        });
        if ('non_field_errors' in errDict) {
            var $errBox = $('<div>')
                .addClass('alert')
                .addClass('alert-danger')
                .text(errDict['non_field_errors']);
            this.$el.prepend($errBox);
        }
    },

    hideErrors: function () {
        this.showErrors({});
    },

    clearFields: function () {
        this.$el.find('input,textarea,select').val('');
    },

}
