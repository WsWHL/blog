const csrftoken = $("[name=csrfmiddlewaretoken]").val();

/**
 * 校验请求类型
 * @param method
 * @returns {*|boolean}
 */
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

/**
 * 设置ajax请求csrfToken验证头
 */
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
})


/**
 * 上传文件
 * @param em
 * @param callback
 * @param url
 */
function upload(em, callback, url) {
    const data = new FormData();
    data.append('file', em.files[0]);
    $.ajax({
        url: url || '/upload/',
        method: 'POST',
        cache: false,
        data: data,
        processData: false,
        contentType: false
    }).done(callback).fail(function (response, textStatus) {
        alert('upload error, status:' + textStatus)
    });
}

/**
 * 删除文章
 * @param article_id
 */
function deleted(article_id) {
    $.ajax({
        url: '/article/delete/' + article_id + '/',
        method: 'POST',
        cache: false,
        processData: false,
        contentType: false
    }).done(function (response, textStatus) {
    })
}