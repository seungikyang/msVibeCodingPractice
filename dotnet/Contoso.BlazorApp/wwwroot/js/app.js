// LocalStorage helper functions
export function setItem(key, value) {
    localStorage.setItem(key, value);
}

export function getItem(key) {
    return localStorage.getItem(key);
}

export function removeItem(key) {
    localStorage.removeItem(key);
}

// Modal helper functions
export function addEscapeKeyListener(dotNetHelper) {
    const handler = (e) => {
        if (e.key === 'Escape') {
            dotNetHelper.invokeMethodAsync('OnEscapeKey');
        }
    };
    document.addEventListener('keydown', handler);
    return handler;
}

export function removeEscapeKeyListener(handler) {
    if (handler) {
        document.removeEventListener('keydown', handler);
    }
}

export function disableBodyScroll() {
    document.body.style.overflow = 'hidden';
}

export function enableBodyScroll() {
    document.body.style.overflow = 'auto';
}

// Focus helper
export function focusElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.focus();
    }
}
