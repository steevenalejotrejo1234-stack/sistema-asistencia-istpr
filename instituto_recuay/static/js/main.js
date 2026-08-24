/* ============================================================
   ISTPR - Main JavaScript
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  /* ---------- Dark Mode ---------- */
  initDarkMode();

  /* ---------- Auto-dismiss alerts ---------- */
  initAutoDismissAlerts();

  /* ---------- Highlight active sidebar link ---------- */
  highlightActiveLink();

  /* ---------- CSRF Token for AJAX ---------- */
  initCSRF();

  /* ---------- Tooltips & Popovers ---------- */
  initTooltips();
});

/* ==========================================================
   Dark Mode
   ========================================================== */
function initDarkMode() {
  var saved = localStorage.getItem('theme');
  if (saved) {
    document.documentElement.setAttribute('data-theme', saved);
  } else {
    var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (prefersDark) {
      document.documentElement.setAttribute('data-theme', 'dark');
    }
  }
  updateDarkModeIcon();
}

function toggleDarkMode() {
  var html = document.documentElement;
  var current = html.getAttribute('data-theme');
  var next = current === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  updateDarkModeIcon();
}

function updateDarkModeIcon() {
  var icon = document.getElementById('darkModeIcon');
  if (!icon) return;
  var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
}

/* ==========================================================
   Sidebar Toggle (Desktop)
   ========================================================== */
function toggleSidebar() {
  var sidebar = document.getElementById('sidebar');
  var mainContent = document.getElementById('mainContent');
  if (!sidebar || !mainContent) return;

  sidebar.classList.toggle('sidebar-collapsed');
  if (sidebar.classList.contains('sidebar-collapsed')) {
    sidebar.style.transform = 'translateX(-260px)';
    mainContent.style.marginLeft = '0';
  } else {
    sidebar.style.transform = 'translateX(0)';
    mainContent.style.marginLeft = '260px';
  }
}

/* ==========================================================
   Auto-dismiss Alerts
   ========================================================== */
function initAutoDismissAlerts() {
  var alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) {
        bsAlert.close();
      }
    }, 5000);
  });
}

/* ==========================================================
   Highlight Active Sidebar Link
   ========================================================== */
function highlightActiveLink() {
  var path = window.location.pathname;
  var links = document.querySelectorAll('.sidebar-nav .nav-link, .offcanvas-body .nav-link');
  links.forEach(function (link) {
    if (link.getAttribute('href') === path) {
      link.classList.add('active');
    }
  });
}

/* ==========================================================
   CSRF Token Setup
   ========================================================== */
function initCSRF() {
  var tokenEl = document.querySelector('meta[name="csrf-token"]');
  if (tokenEl) {
    window.csrfToken = tokenEl.getAttribute('content');
  }
}

/* ==========================================================
   Tooltips & Popovers
   ========================================================== */
function initTooltips() {
  var tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipTriggerList.forEach(function (el) {
    bootstrap.Tooltip.getOrCreateInstance(el);
  });

  var popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
  popoverTriggerList.forEach(function (el) {
    bootstrap.Popover.getOrCreateInstance(el);
  });
}

/* ==========================================================
   Confirm Delete Helper
   ========================================================== */
function confirmDelete(url, itemName) {
  var name = itemName || 'este registro';
  var modalHtml = `
    <div class="modal fade" id="confirmDeleteModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header border-0 pb-0">
            <h5 class="modal-title text-danger">
              <i class="fas fa-exclamation-triangle me-2"></i>Confirmar Eliminación
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body py-3">
            <p class="mb-0">¿Está seguro que desea eliminar <strong>${name}</strong>? Esta acción no se puede deshacer.</p>
          </div>
          <div class="modal-footer border-0 pt-0">
            <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancelar</button>
            <a href="${url}" class="btn btn-danger btn-sm">
              <i class="fas fa-trash-alt me-1"></i>Eliminar
            </a>
          </div>
        </div>
      </div>
    </div>`;

  var existing = document.getElementById('confirmDeleteModal');
  if (existing) existing.remove();

  document.body.insertAdjacentHTML('beforeend', modalHtml);
  var modal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
  modal.show();

  document.getElementById('confirmDeleteModal').addEventListener('hidden.bs.modal', function () {
    this.remove();
  });
}

/* ==========================================================
   QR Scanner Integration (html5-qrcode)
   ========================================================== */
var qrScannerInstance = null;

function startQRScanner(elementId, onSuccess, onError) {
  if (typeof Html5Qrcode === 'undefined') {
    console.warn('html5-qrcode library not loaded. Include https://unpkg.com/html5-qrcode');
    if (onError) onError('html5-qrcode library not loaded');
    return;
  }

  stopQRScanner();

  qrScannerInstance = new Html5Qrcode(elementId);

  var config = {
    fps: 10,
    qrbox: { width: 250, height: 250 },
    aspectRatio: 1.0,
    showTorchButtonIfSupported: true,
    showZoomSliderIfSupported: true
  };

  qrScannerInstance.start(
    { facingMode: 'environment' },
    config,
    function (decodedText) {
      stopQRScanner();
      if (onSuccess) onSuccess(decodedText);
    },
    function (errorMessage) {
      // Scan error - ignore (continuous scanning)
    }
  ).catch(function (err) {
    console.error('QR Scanner start error:', err);
    if (onError) onError(err);
  });
}

function stopQRScanner() {
  if (qrScannerInstance) {
    qrScannerInstance.stop().then(function () {
      qrScannerInstance.clear();
      qrScannerInstance = null;
    }).catch(function (err) {
      console.warn('QR Scanner stop error:', err);
    });
  }
}

/* ==========================================================
   Chart.js Initialization Helper
   ========================================================== */
function initChart(canvasId, type, labels, datasets, options) {
  var canvas = document.getElementById(canvasId);
  if (!canvas) return null;

  var ctx = canvas.getContext('2d');

  var defaultOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: datasets.length > 1,
        position: 'top',
        labels: {
          padding: 15,
          usePointStyle: true,
          font: { size: 12 }
        }
      },
      tooltip: {
        backgroundColor: 'rgba(0,0,0,0.8)',
        padding: 10,
        titleFont: { size: 13 },
        bodyFont: { size: 12 },
        cornerRadius: 6
      }
    },
    scales: (type === 'line' || type === 'bar') ? {
      y: {
        beginAtZero: true,
        grid: { color: 'rgba(0,0,0,0.05)' },
        ticks: { font: { size: 11 } }
      },
      x: {
        grid: { display: false },
        ticks: { font: { size: 11 } }
      }
    } : undefined
  };

  var merged = deepMerge(defaultOptions, options || {});

  return new Chart(ctx, {
    type: type,
    data: {
      labels: labels,
      datasets: datasets
    },
    options: merged
  });
}

function deepMerge(target, source) {
  var result = Object.assign({}, target);
  for (var key in source) {
    if (source.hasOwnProperty(key)) {
      if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key]) && target[key]) {
        result[key] = deepMerge(target[key], source[key]);
      } else {
        result[key] = source[key];
      }
    }
  }
  return result;
}

/* ==========================================================
   Notification - Mark as Read (AJAX)
   ========================================================== */
function markNotificationRead(notifId) {
  fetch('/notificaciones/' + notifId + '/leer/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': window.csrfToken || '',
      'Content-Type': 'application/json'
    }
  })
    .then(function (response) { return response.json(); })
    .then(function (data) {
      if (data.success) {
        var el = document.getElementById('notif-' + notifId);
        if (el) {
          el.classList.remove('fw-bold');
          el.classList.add('opacity-50');
        }
        updateNotificationBadge();
      }
    })
    .catch(function (err) {
      console.error('Error marking notification as read:', err);
    });
}

function markAllNotificationsRead() {
  fetch('/notificaciones/leer-todas/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': window.csrfToken || '',
      'Content-Type': 'application/json'
    }
  })
    .then(function (response) { return response.json(); })
    .then(function (data) {
      if (data.success) {
        document.querySelectorAll('.notification-item').forEach(function (el) {
          el.classList.remove('fw-bold');
          el.classList.add('opacity-50');
        });
        updateNotificationBadge();
      }
    })
    .catch(function (err) {
      console.error('Error marking all notifications:', err);
    });
}

function updateNotificationBadge() {
  var badge = document.getElementById('notifBadge');
  if (!badge) return;
  var current = parseInt(badge.textContent) || 0;
  var newCount = Math.max(0, current - 1);
  if (newCount === 0) {
    badge.style.display = 'none';
  } else {
    badge.textContent = newCount;
  }
}

/* ==========================================================
   Form Validation Helpers
   ========================================================== */
function validateRequired(formId) {
  var form = document.getElementById(formId);
  if (!form) return false;

  var isValid = true;
  var requiredFields = form.querySelectorAll('[required]');

  requiredFields.forEach(function (field) {
    clearFieldError(field);

    if (!field.value || field.value.trim() === '') {
      showFieldError(field, 'Este campo es obligatorio');
      isValid = false;
    } else if (field.type === 'email' && !isValidEmail(field.value)) {
      showFieldError(field, 'Ingrese un correo electrónico válido');
      isValid = false;
    } else if (field.hasAttribute('data-min-length')) {
      var minLen = parseInt(field.getAttribute('data-min-length'));
      if (field.value.trim().length < minLen) {
        showFieldError(field, 'Mínimo ' + minLen + ' caracteres');
        isValid = false;
      }
    }
  });

  if (!isValid) {
    var firstInvalid = form.querySelector('.is-invalid');
    if (firstInvalid) firstInvalid.focus();
  }

  return isValid;
}

function showFieldError(field, message) {
  field.classList.add('is-invalid');
  var existing = field.parentNode.querySelector('.invalid-feedback');
  if (existing) existing.remove();

  var feedback = document.createElement('div');
  feedback.className = 'invalid-feedback';
  feedback.textContent = message;
  field.parentNode.appendChild(feedback);
}

function clearFieldError(field) {
  field.classList.remove('is-invalid');
  var feedback = field.parentNode.querySelector('.invalid-feedback');
  if (feedback) feedback.remove();
}

function clearAllErrors(formId) {
  var form = document.getElementById(formId);
  if (!form) return;
  form.querySelectorAll('.is-invalid').forEach(function (f) {
    f.classList.remove('is-invalid');
  });
  form.querySelectorAll('.invalid-feedback').forEach(function (fb) {
    fb.remove();
  });
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validatePasswordsMatch(passwordId, confirmId) {
  var pass = document.getElementById(passwordId);
  var confirm = document.getElementById(confirmId);
  if (!pass || !confirm) return true;

  clearFieldError(confirm);

  if (pass.value !== confirm.value) {
    showFieldError(confirm, 'Las contraseñas no coinciden');
    return false;
  }
  return true;
}

/* ==========================================================
   AJAX POST Helper
   ========================================================== */
function ajaxPost(url, data, onSuccess, onError) {
  return fetch(url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': window.csrfToken || '',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(function (response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.json();
    })
    .then(function (data) {
      if (onSuccess) onSuccess(data);
    })
    .catch(function (err) {
      console.error('AJAX POST error:', err);
      if (onError) onError(err);
    });
}

/* ==========================================================
   Loading Overlay
   ========================================================== */
function showLoading() {
  if (document.getElementById('loadingOverlay')) return;
  var overlay = document.createElement('div');
  overlay.id = 'loadingOverlay';
  overlay.className = 'loading-overlay';
  overlay.innerHTML = '<div class="spinner-grow-custom"></div><div class="loading-text">Cargando...</div>';
  document.body.appendChild(overlay);
}

function hideLoading() {
  var overlay = document.getElementById('loadingOverlay');
  if (overlay) overlay.remove();
}

/* ==========================================================
   Print Helper
   ========================================================== */
function printSection(elementId) {
  var el = document.getElementById(elementId);
  if (!el) return;

  var printWindow = window.open('', '_blank', 'width=900,height=700');
  printWindow.document.write('<html><head><title>ISTPR - Imprimir</title>');
  printWindow.document.write('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">');
  printWindow.document.write('<style>body{padding:20px;font-family:Segoe UI,sans-serif;}</style>');
  printWindow.document.write('</head><body>');
  printWindow.document.write(el.innerHTML);
  printWindow.document.write('</body></html>');
  printWindow.document.close();

  printWindow.onload = function () {
    printWindow.focus();
    printWindow.print();
    printWindow.close();
  };
}
