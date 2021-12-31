export function showNotify(title, content) {
    const titleBar = document.getElementById('global-notify-title')
    titleBar.innerHTML = title;
    const ContentBar = document.getElementById('global-notify-content')
    ContentBar.innerHTML = content;
    document.getElementById('global-notify').checked = true;
}

export function showLoading(tip) {
    const loadingBar = document.getElementById('loading-modal-content');
    loadingBar.innerHTML = tip
    const loadingModal = document.getElementById('loading-modal');
    loadingModal.checked = true;
}

export function showTranslucentLoading(tip) {
    const loadingBar = document.getElementById('translucent-loading-modal-content');
    loadingBar.innerHTML = tip
    const loadingModal = document.getElementById('translucent-loading-modal');
    loadingModal.checked = true;
}

export function hideLoading() {
    const loadingBar = document.getElementById('loading-modal-content');
    loadingBar.innerHTML = ''
    const translucentLoadingBar = document.getElementById('translucent-loading-modal-content');
    translucentLoadingBar.innerHTML = ''
    document.getElementById('loading-modal').checked = false;
    document.getElementById('translucent-loading-modal').checked = false;
}
