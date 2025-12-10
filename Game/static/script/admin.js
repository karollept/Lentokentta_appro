const config = {
  dashboardTitle: 'Admin Dashboard',
  welcomeMessage: 'Tervetuloa admin-paneeliin!',
  apiBase: 'http://127.0.0.1:5000'
};

let currentApi = config.apiBase;

async function apiFetch(path, opts = {}) {
  const url = path.startsWith('http') ? path : `${currentApi}${path}`;
  const options = Object.assign({ credentials: 'include' }, opts);
  options.headers = Object.assign({ 'Content-Type': 'application/json' }, options.headers || {});

  try {
    const res = await fetch(url, options);
    if (!res.ok) {
      let bodyText = null;
      try { bodyText = await res.text(); } catch (e) {}
      let msg = res.statusText || 'Virhe palvelimelta';
      try {
        if (bodyText) {
          const j = JSON.parse(bodyText);
          if (j && j.error) msg = j.error;
        }
      } catch (e) {}
      throw new Error(`${res.status}: ${msg}`);
    }

    const ct = (res.headers.get('content-type') || '');
    if (ct.includes('application/json')) return await res.json();
    return await res.text();
  } catch (err) {
    console.error('apiFetch error ->', err, 'url:', url);
    showError(`Virhe palvelimen kanssa: ${err.message}`);
    return null;
  }
}

function showError(msg, duration = 5000) {
  const container = document.getElementById('content');
  if (!container) return console.warn('showError: no content element');
  const el = document.createElement('div');
  el.className = 'error-message';
  el.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${msg}`;
  container.insertBefore(el, container.firstChild);
  setTimeout(() => { try { el.remove(); } catch (e) {} }, duration);
}

function showSuccess(msg, duration = 3000) {
  const container = document.getElementById('content');
  if (!container) return console.warn('showSuccess: no content element');
  const el = document.createElement('div');
  el.className = 'success-message';
  el.innerHTML = `<i class="fas fa-check-circle"></i> ${msg}`;
  container.insertBefore(el, container.firstChild);
  setTimeout(() => { try { el.remove(); } catch (e) {} }, duration);
}

function formatDate(ts) {
  if (!ts) return '-';
  try {
    const d = new Date(ts);
    return d.toLocaleString('fi-FI', { dateStyle: 'short', timeStyle: 'short' });
  } catch (e) {
    return ts;
  }
}

function escapeHtml(input) {
  if (input === null || input === undefined) return '';
  return String(input)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
    .replace(/`/g, '&#096;');
}

const navHome = document.getElementById('nav-home');
const navUsers = document.getElementById('nav-users');
const navData = document.getElementById('nav-data');

if (navHome) navHome.addEventListener('click', () => { loadStats(); setActive(navHome); });
if (navUsers) navUsers.addEventListener('click', () => { loadUsers(); setActive(navUsers); });
if (navData) navData.addEventListener('click', () => { loadGameData(); setActive(navData); });

function setActive(el) {
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  if (el) el.classList.add('active');
}

const logoutBtn = document.getElementById('logout-btn');
if (logoutBtn) {
  logoutBtn.addEventListener('click', async () => {
    try { await apiFetch('/logout', { method: 'POST' }); } catch (e) { console.warn('Logout failed', e); }
    try { localStorage.removeItem('auth_token'); sessionStorage.clear(); } catch (e) {}
    window.location.href = '../templates/login.html';
  });
}

async function loadStats() {
  setActive(navHome);
  const content = document.getElementById('content');
  if (!content) return;
  content.innerHTML = `<div class="loading"><div class="spinner"></div>Ladataan tilastoja...</div>`;

  const stats = await apiFetch('/admin/stats');
  if (!stats) {
    content.innerHTML = `
      <div class="welcome-section">
        <h2>Tilastoja ei voitu ladata</h2>
        <p>Tarkista API-yhteys ja yritä uudelleen.</p>
      </div>
    `;
    return;
  }

  const welcomeEl = document.getElementById('welcome-message');
  const wm = (welcomeEl && welcomeEl.textContent) ? welcomeEl.textContent : config.welcomeMessage;

  content.innerHTML = `
    <div class="welcome-section">
      <h2 id="welcome-area">${escapeHtml(wm)}</h2>
      <p>Järjestelmän yleiskatsaus ja keskeiset tilastot.</p>
    </div>
    <div class="stats-grid">
      <div class="stat-card"><div class="stat-number">${stats.users || 0}</div><div class="stat-label">Käyttäjiä</div></div>
      <div class="stat-card"><div class="stat-number">${stats.games || 0}</div><div class="stat-label">Pelejä</div></div>
      <div class="stat-card"><div class="stat-number">${stats.airports || 0}</div><div class="stat-label">Lentokenttiä</div></div>
      <div class="stat-card"><div class="stat-number">${stats.countries || 0}</div><div class="stat-label">Maita</div></div>
    </div>
  `;
}

async function loadUsers() {
  setActive(navUsers);
  const content = document.getElementById('content');
  if (!content) return;
  content.innerHTML = `<div class="loading"><div class="spinner"></div>Ladataan käyttäjiä...</div>`;

  const users = await apiFetch('/admin/users');
  if (!users) {
    content.innerHTML = `
      <div class="data-section">
        <h2>Käyttäjät</h2>
        <div class="error-message"><i class="fas fa-exclamation-triangle"></i> Käyttäjätietoja ei voitu ladata. Tarkista API-yhteys.</div>
      </div>
    `;
    return;
  }

  const rows = users.map(u => `
    <tr>
      <td><input class="inline-edit" value="${escapeHtml(u.username || '')}" onchange="updateUser(${u.id}, this.value)" placeholder="Käyttäjänimi" readonly /></td>
      <td><input type="password" class="inline-edit" placeholder="Uusi salasana" onchange="updatePassword(${u.id}, this.value)" readonly /></td>
      <td><input class="inline-edit" type="number" min="0" max="120" value="${u.age || ''}" onchange="updateAge(${u.id}, this.value)" placeholder="Ikä" readonly /></td>
      <td><input class="inline-edit" type="number" step="0.01" value="${u.budget == null ? 0 : u.budget}" onchange="updateBudget(${u.id}, this.value)" placeholder="Budjetti" readonly/></td>
      <td>${escapeHtml(u.current_airport || '-')}</td>
      <td>${formatDate(u.created_at)}</td>
      <td class="actions-cell">
        <button class="action-btn info-btn" title="Tiedot & sessiot" onclick="showUserDetails(${u.id})"><i class="fas fa-info-circle"></i></button>
        <button class="action-btn edit-btn" title="Muokkaa" onclick="editUser(${u.id})"><i class="fas fa-edit"></i></button>
        <button class="action-btn delete-btn" title="Poista" onclick="deleteUser(${u.id})"><i class="fas fa-trash"></i></button>
      </td>
    </tr>
  `).join('');

  content.innerHTML = `
    <div class="data-section users-table">
      <h2 class="user-table-title"><i class="fas fa-users"></i> Käyttäjien hallinta</h2>
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.8rem">
        <div class="muted">Hallinnoi käyttäjiä</div>
        <div>
          <button id="addUserBtn" class="btn btn-primary">+ Lisää käyttäjä</button>
        </div>
      </div>
      <div class="table-container">
        <table aria-label="Käyttäjät">
          <thead>
            <tr>
              <th>Käyttäjänimi</th>
              <th>Salasana</th>
              <th>Ikä</th>
              <th>Budjetti</th>
              <th>Sijainti</th>
              <th>Liittynyt</th>
              <th class="actions-cell">Toiminnot</th>
            </tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    </div>
  `;

  const addBtn = document.getElementById('addUserBtn');
  if (addBtn) addBtn.addEventListener('click', showAddUserModal);
}

function showAddUserModal() {
  const modal = document.createElement('div');
  modal.className = 'details-modal';
  modal.innerHTML = `
    <div class="details-box" role="dialog" aria-modal="true">
      <h3 class="add-user-h3">Lisää uusi käyttäjä</h3>
      <div class="modal-form">
        <input id="new_username" placeholder="Käyttäjänimi" maxlength="10" pattern="[A-Za-z]+" oninput="this.value = this.value.replace(/[^A-Za-z]/g,'')" />
        <input id="new_password" type="password" placeholder="Salasana" maxlength="10" />
        <input id="new_age" type="number" min="0" max="999" placeholder="Ikä" oninput="if(this.value.length > 3) this.value = this.value.slice(0,3);" />
        <input id="new_budget" type="number" step="0.01" placeholder="Budjetti" min="0" max="30000" oninput="if(parseFloat(this.value) > 30000) this.value = 30000;" />
      </div>
      <div class="modal-actions">
        <button class="btn cancel" id="cancelAdd">Peruuta</button>
        <button class="btn btn-primary" id="confirmAdd">Luo käyttäjä</button>
      </div>
    </div>
  `;

  document.body.appendChild(modal);

  document.getElementById('cancelAdd').addEventListener('click', () => modal.remove());
  document.getElementById('confirmAdd').addEventListener('click', async () => {
    const username = (document.getElementById('new_username').value || '').trim();
    const password = document.getElementById('new_password').value || '';
    const age = document.getElementById('new_age').value;
    const budget = parseFloat(document.getElementById('new_budget').value || 0);

    if (!/^[A-Za-z]+$/.test(username)) { alert('Käyttäjänimi saa sisältää vain kirjaimia (A–Z).'); return; }
    if (username.length > 10) { alert('Käyttäjänimen maksimipituus on 10 merkkiä.'); return; }
    if (password.length > 10) { alert('Salasanan maksimipituus on 10 merkkiä.'); return; }
    if (age && age.length > 3) { alert('Ikä voi olla enintään 3 numeroa.'); return; }
    if (budget > 30000) { alert('Budjetti ei voi ylittää 30000€.'); return; }

    const payload = { username, password, age: age ? parseInt(age, 10) : null, budget };
    const res = await apiFetch('/admin/add_user', { method: 'POST', body: JSON.stringify(payload) });
    if (res) {
      showSuccess('Käyttäjä luotu onnistuneesti!');
      modal.remove();
      await loadUsers();
    }
  });
}

async function updateUser(id, newName) {
  if (!newName || !String(newName).trim()) return;
  const result = await apiFetch(`/admin/user/${id}`, { method: 'PUT', body: JSON.stringify({ username: String(newName).trim() }) });
  if (result) showSuccess('Käyttäjätiedot päivitetty!');
}

async function updatePassword(id, newPass) {
  if (!newPass) return;
  if (!confirm('Haluatko varmasti vaihtaa käyttäjän salasanan?')) return;
  const result = await apiFetch(`/admin/update_password/${id}`, { method: 'POST', body: JSON.stringify({ password: newPass }) });
  if (result) showSuccess('Salasana vaihdettu onnistuneesti!');
}

async function updateAge(id, newAge) {
  if (newAge === '' || newAge === null) return;
  const parsed = parseInt(newAge, 10);
  if (isNaN(parsed)) return;
  const result = await apiFetch(`/admin/user/${id}/age`, { method: 'PUT', body: JSON.stringify({ age: parsed }) });
  if (result) showSuccess('Ikä päivitetty onnistuneesti!');
}

async function updateBudget(id, newBudget) {
  const parsed = parseFloat(newBudget);
  if (isNaN(parsed)) return;
  const result = await apiFetch(`/admin/user/${id}/budget`, { method: 'PUT', body: JSON.stringify({ budget: parsed }) });
  if (result) showSuccess('Budjetti päivitetty onnistuneesti!');
}

async function deleteUser(id) {
  if (!confirm('Haluatko varmasti poistaa tämän käyttäjän? Tätä toimintoa ei voi perua.')) return;
  const result = await apiFetch(`/admin/user/${id}`, { method: 'DELETE' });
  if (result) { showSuccess('Käyttäjä poistettu.'); await loadUsers(); }
}

function editUser(id) {
  // find the row by matching the button's onclick attribute — cheap but human
  const btn = document.querySelector(`button[onclick="editUser(${id})"]`);
  if (!btn) return;
  const row = btn.closest('tr');
  const inputs = row.querySelectorAll('input.inline-edit');
  const icon = row.querySelector('.edit-btn i');

  const isEditing = row.classList.toggle('editing');

  inputs.forEach(inp => {
    if (isEditing) inp.removeAttribute('readonly');
    else inp.setAttribute('readonly', true);
  });

  if (icon) {
    if (isEditing) icon.classList.replace('fa-edit', 'fa-save');
    else icon.classList.replace('fa-save', 'fa-edit');
  }

  if (!isEditing) showSuccess('Muokkaukset tallennettu!');
}

async function loadGameData() {
  setActive(navData);
  const content = document.getElementById('content');
  if (!content) return;
  content.innerHTML = `<div class="loading"><div class="spinner"></div>Ladataan pelin dataa...</div>`;

  const data = await apiFetch('/admin/game_data');
  if (!data) {
    content.innerHTML = `<div class="data-section"><h2>Pelin data</h2><div class="error-message"><i class="fas fa-exclamation-triangle"></i> Pelidataa ei voitu ladata.</div></div>`;
    return;
  }

  const countries = [...new Set(data.map(r => r.valtio))].filter(Boolean).sort();
  const minigames = [...new Set(data.map(r => r.minipeli))].filter(Boolean).sort();

  function renderRows(d) {
    if (!d || d.length === 0) return `<tr><td colspan="6" style="text-align:center;color:var(--text-secondary);padding:1rem">Ei tuloksia</td></tr>`;

    const seen = new Set();
    return d.filter(row => {
      if (seen.has(row.ident)) return false;
      seen.add(row.ident);
      return true;
    }).map(row => `
      <tr onclick="showConnectionsModal('${escapeHtml(row.ident || '')}')">
        <td>${escapeHtml(row.valtio || '-')}</td>
        <td>${escapeHtml(row.lentokentta || '-')}</td>
        <td>${escapeHtml(row.ident || '-')}</td>
        <td>${escapeHtml(row.minipeli || '-')}</td>
        <td>${escapeHtml(row.token || '-')}</td>
        <td>${escapeHtml(row.tarinat || '-')}</td>
      </tr>
    `).join('');
  }

  content.innerHTML = `
    <h2><i class="fas fa-database"></i> Pelin data</h2><br>
    <div class="filter-panel" style="margin-bottom: 1.5rem; display: flex; flex-wrap: wrap; gap: 1rem;">
      <select id="filter-country" class="inline-edit" style="max-width: 200px;">
        <option value="">Valtiot</option>
        ${countries.map(c => `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`).join('')}
      </select>
      <select id="filter-minigame" class="inline-edit" style="max-width: 200px;">
        <option value="">Minipelit</option>
        ${minigames.map(m => `<option value="${escapeHtml(m)}">${escapeHtml(m)}</option>`).join('')}
      </select>
      <input type="text" id="filter-search" class="inline-edit" placeholder="Hae..." oninput="applyFilters()" style="flex:1" />
      <button class="action-btn filter-btn" onclick="applyFilters()">Suodata</button>
      <button class="action-btn filter-btn" style="background: var(--accent-primary); color: var(--bg-primary);" onclick="resetFilters()">Tyhjennä</button>
    </div>

    <div class="table-container">
      <div class="game-table">
        <table id="game-data-table">
          <thead>
            <tr>
              <th>Valtio</th>
              <th>Lentokenttä</th>
              <th>Ident</th>
              <th>Minipeli</th>
              <th>Haalarimerkki</th>
              <th>Tarina</th>
            </tr>
          </thead>
          <tbody>${renderRows(data)}</tbody>
        </table>
      </div>
    </div>
  `;

  window.gameData = data; 
}

async function showConnectionsModal(ident) {
  const connections = await apiFetch(`/api/connections?ident=${encodeURIComponent(ident)}`);
  const rowsHtml = (connections && connections.length) ? connections.map(c => `
    <tr>
      <td>${escapeHtml(c.destination)}</td>
      <td>${escapeHtml(c.country_name || '-')}</td>
      <td>${escapeHtml(c.price)} €</td>
    </tr>
  `).join('') : `<tr><td colspan="3" style="text-align:center;color:var(--text-secondary)">Ei yhteyksiä</td></tr>`;

  const modal = document.createElement('div');
  modal.className = 'details-modal';
  modal.innerHTML = `
    <div class="details-box">
      <h3 style="color:var(--accent-primary);text-align:center">Yhteydet - ${escapeHtml(ident)}</h3>
      <div class="table-container">
        <table>
          <thead><tr><th>Yhteys</th><th>Maa</th><th>Yhteyden hinta</th></tr></thead>
          <tbody>${rowsHtml}</tbody>
        </table>
      </div>
      <div style="display:flex;justify-content:flex-end;margin-top:0.6rem">
        <button class="btn cancel" onclick="this.closest('.details-modal').remove()">Sulje</button>
      </div>
    </div>
  `;
  document.body.appendChild(modal);
}

function applyFilters() {
  const country = (document.getElementById('filter-country') || {}).value || '';
  const minigame = (document.getElementById('filter-minigame') || {}).value || '';
  const search = ((document.getElementById('filter-search') || {}).value || '').toLowerCase().trim();
  const filtered = (window.gameData || []).filter(row => {
    if (!search) return (!country || row.valtio === country) && (!minigame || row.minipeli === minigame);
    const combined = Object.values(row).filter(v => v !== null && v !== undefined).join(' ').toLowerCase();
    return (!country || row.valtio === country) && (!minigame || row.minipeli === minigame) && combined.includes(search);
  });

  const tbody = document.querySelector('#game-data-table tbody');
  if (!tbody) return;
  if (!filtered.length) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;color:var(--text-secondary);padding:1rem">Ei tuloksia</td></tr>`;
    return;
  }

  tbody.innerHTML = filtered.map(row => {
    const tarina = row.tarinat || '';
    const short = tarina.length > 500 ? tarina.substring(0, 500) + '...' : tarina;
    return `
      <tr onclick="showConnectionsModal('${escapeHtml(row.ident || '')}')">
        <td>${escapeHtml(row.valtio || '-')}</td>
        <td>${escapeHtml(row.lentokentta || '-')}</td>
        <td>${escapeHtml(row.ident || '-')}</td>
        <td>${escapeHtml(row.minipeli || '-')}</td>
        <td>${escapeHtml(row.token || '-')}</td>
        <td>${tarina.length > 500 ? `<span class=\"tarina-text\" onclick=\"event.stopPropagation(); showFullTarina(${JSON.stringify(tarina)})\">${escapeHtml(short)}</span>` : escapeHtml(tarina || '-')}</td>
      </tr>
    `;
  }).join('');
}

function resetFilters() {
  const fc = document.getElementById('filter-country'); if (fc) fc.value = '';
  const fm = document.getElementById('filter-minigame'); if (fm) fm.value = '';
  const fs = document.getElementById('filter-search'); if (fs) fs.value = '';
  applyFilters();
}

function showFullTarina(tarina) {
  const modal = document.createElement('div');
  modal.className = 'details-modal';
  modal.innerHTML = `
    <div class="details-box">
      <button style="position:absolute;right:12px;top:12px;background:var(--danger);color:#fff;border:none;padding:.4rem .6rem;border-radius:6px" onclick="this.parentElement.parentElement.remove()"><i class="fas fa-times"></i></button>
      <h3 style="color:var(--accent-primary);text-align:center;margin-bottom:.6rem">Tarina</h3>
      <div style="white-space:pre-line;color:var(--text-secondary);line-height:1.4">${escapeHtml(tarina)}</div>
    </div>
  `;
  document.body.appendChild(modal);
}

async function showUserDetails(id) {
  const user = await apiFetch(`/admin/user/${id}`);
  const sessions = await apiFetch(`/admin/user/${id}/sessions`);
  if (!user) return;

  const badgesHtml = (user.haalarimerkit && user.haalarimerkit.length) ? `<ul style="padding-left:1rem;text-align:left">${user.haalarimerkit.map(m => `<li>${escapeHtml(m)}</li>`).join('')}</ul>` : `<p class="muted">Ei haalarimerkkejä</p>`;

  const modal = document.createElement('div'); modal.className = 'details-modal';
  modal.innerHTML = `
    <div class="details-box">
      <h3 style="color:var(--accent-primary)"><i class="fas fa-user"></i> ${escapeHtml(user.username || '—')}</h3>
      <p><strong>Budjetti:</strong> ${user.budget || 0} €</p>
      <p><strong>Sijainti:</strong> ${escapeHtml(user.current_airport || '-')}</p>
      <p><strong>Viimeisin kirjautuminen:</strong> ${formatDate(user.last_login)}</p>
      <div style="margin-top:.8rem">
        <h4 style="color:var(--accent-secondary)">Haalarimerkit</h4>
        ${badgesHtml}
      </div>
      <div style="margin-top:1rem">
        <h4 style="color:var(--accent-secondary)">Sessio(t)</h4>
        <div id="session-list">
          ${(!sessions || !sessions.length) ? `<p class="muted">Sessioita ei löytynyt</p>` : sessions.map(s => `
            <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px dashed rgba(255,255,255,0.03);padding:.5rem 0">
              <div style="flex:1">
                <div>
                  <strong>Pelaaja:</strong> ${escapeHtml(s.screen_name || 'Tuntematon')}<br>
                  <strong>Sessio ID:</strong> ${escapeHtml(s.id || s.session_id || '-')}
                </div>
                <div class="muted"><strong>Alkanut:</strong> ${formatDate(s.start_time)} &nbsp; <strong><br>Päättynyt:</strong> ${formatDate(s.end_time)}</div>
              </div>
              <div style="margin-left:8px">
                <button class="btn cancel" onclick="revokeSession('${escapeHtml(s.id || s.session_id)}', ${id}, this)">Kumoa</button>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
      <div style="display:flex;justify-content:flex-end;gap:.5rem;margin-top:1rem">
        <button class="btn cancel" id="sulje" onclick="this.closest('.details-modal').remove()">Sulje</button>
      </div>
    </div>
  `;
  document.body.appendChild(modal);
}

async function revokeSession(sessionId, userId, btn) {
  if (!confirm('Haluatko poistaa tämän session?')) return;
  btn.disabled = true;
  const tryPaths = [
    `/admin/session/${sessionId}`,
    `/admin/user/${userId}/session/${sessionId}`,
    `/session/${sessionId}`
  ];
  let ok = false;
  for (const p of tryPaths) {
    const res = await apiFetch(p, { method: 'DELETE' });
    if (res) { ok = true; break; }
  }
  if (ok) {
    showSuccess('Sessio poistettu.');
    try { document.querySelector('.details-modal').remove(); await showUserDetails(userId); } catch (e) {}
  } else {
    showError('Ei voitu poistaa sessiota (backend ei tukenut pyydettyä polkua).');
    btn.disabled = false;
  }
}

(function init() {
  currentApi = config.apiBase || currentApi;
  const title = document.getElementById('dashboard-title'); if (title) title.textContent = config.dashboardTitle || 'Admin Dashboard';
  const wmEl = document.getElementById('welcome-message'); if (wmEl) wmEl.textContent = config.welcomeMessage;
  loadStats();
})();
