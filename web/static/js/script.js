/**
 * 上传文件
 * @param em
 * @param callback
 * @param url
 */
function upload(em, callback, url) {
    const data = new FormData();
    data.append('file', em.files[0]);
    if (document.getElementsByName('csrfmiddlewaretoken').length > 0) {
        data.append('csrfmiddlewaretoken', document.getElementsByName('csrfmiddlewaretoken')[0].value);
    }
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