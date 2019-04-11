//    自定义图片上传适配器
class UploadAdapter {
    constructor(loader, url, t) {
        this.loader = loader;
        this.url = url;
        this.t = t;
    }

    upload() {
        return this.loader.file.then(file => new Promise((resolve, reject) => {
            const loader = this.loader;
            const xhr = new XMLHttpRequest();
            // Prepare form data.
            const data = new FormData();
            data.append('file', file);
            if (document.getElementsByName('csrfmiddlewaretoken').length > 0) {
                data.append('csrfmiddlewaretoken', document.getElementsByName('csrfmiddlewaretoken')[0].value);
            } else {
                return reject('token can not be empty')
            }
            // Initializes the XMLHttpRequest object.
            xhr.open('POST', this.url, true)
            xhr.contentType = 'json';
            xhr.responseType = 'json';
            const genericError = this.t('a') + ` ${file.name}.`;
            xhr.addEventListener('error', () => reject(genericError))
            xhr.addEventListener('abort', () => reject());
            xhr.addEventListener('load', () => {
                const response = xhr.response;
                if (!response || !response.uploaded) {
                    return reject(response && response.error && response.error.message ? response.error.message : genericError);
                }
                resolve({default: response.url});
            });
            if (xhr.upload) {
                xhr.upload.addEventListener('progress', evt => {
                    if (evt.lengthComputable) {
                        loader.uploadTotal = evt.total;
                        loader.uploaded = evt.loaded;
                    }
                });
            }
            // Sed request
            xhr.send(data);
        }));
    }

    abort() {
    }
}