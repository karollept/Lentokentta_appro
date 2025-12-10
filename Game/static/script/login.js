   const ADJ = ['FALCON','SKY','NIGHT','STAR','EAGLE','DRONE','NEBULA','AERO','RAPTOR','HORIZON','GLIDER','STRATO'];
    const SUF = ['01','7','X','77','_7','_11','_42','9','21','300'];
    function generatePlayerName(){
      const a = ADJ[Math.floor(Math.random()*ADJ.length)];
      const s = SUF[Math.floor(Math.random()*SUF.length)];
      const maybeNum = Math.random()<0.45 ? '_' + Math.floor(Math.random()*500) : '';
      return `${a}${s}${maybeNum}`;
    }

    const nimiEl = document.getElementById('nimi');
    const salasanaEl = document.getElementById('salasana');
    const playerArea = document.getElementById('playerArea');
    const playerIdEl = document.getElementById('playerId');
    const suggestionsEl = document.getElementById('suggestions');
    const useUsernameBtn = document.getElementById('useUsernameBtn');
    const regenerateBtn = document.getElementById('regenerateBtn');
    const diffBtns = document.querySelectorAll('.diff-btn');
    const loginForm = document.getElementById('loginForm');

    salasanaEl.addEventListener('input', ()=>{
      const has = salasanaEl.value.trim().length > 0;
      playerArea.style.display = has ? 'flex' : 'none';
      playerArea.setAttribute('aria-hidden', !has);
      if (has && suggestionsEl.children.length===0) populateSuggestions();
    });

    function populateSuggestions(){
      suggestionsEl.innerHTML = '';
      for(let i=0;i<4;i++){
        const name = generatePlayerName();
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'suggestion';
        btn.textContent = name;
        btn.addEventListener('click', ()=>{ setPlayerId(name); lockPlayerId(false); });
        suggestionsEl.appendChild(btn);
      }
      if(!playerIdEl.value) setPlayerId(suggestionsEl.firstChild.textContent);
    }

    regenerateBtn.addEventListener('click', ()=>{ populateSuggestions(); playerIdEl.focus(); });

    function setPlayerId(val){ playerIdEl.value = val; }
    function lockPlayerId(locked){
      playerIdEl.disabled = !!locked;
      useUsernameBtn.textContent = locked ? 'Käyttäjänimi käytössä' : 'Käytä käyttäjänimeä';
      useUsernameBtn.setAttribute('aria-pressed', locked ? 'true' : 'false');
      useUsernameBtn.style.opacity = locked ? '0.7' : '1';
    }

    useUsernameBtn.addEventListener('click', ()=>{
      const username = (nimiEl.value || '').trim();
      if(!username){ alert('Syötä ensin käyttäjänimi jotta voit käyttää sitä Player ID:nä.'); nimiEl.focus(); return; }
      setPlayerId(username);
      lockPlayerId(true);
    });

    diffBtns.forEach(b=> b.addEventListener('click', ()=>{ diffBtns.forEach(x=>x.classList.remove('active')); b.classList.add('active'); }));

    loginForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const nimi = nimiEl.value.trim();
      const salasana = salasanaEl.value.trim();
      const player_id = playerIdEl.value.trim();
      const vaikeus = document.querySelector('.diff-btn.active')?.textContent;

      if(!nimi || !salasana){ alert('Täytä käyttäjänimi ja salasana'); return; }
      if(!player_id){ alert('Valitse Player ID ennen jatkamista'); playerIdEl.focus(); return; }
      if(!vaikeus){ alert('Valitse vaikeustaso'); return; }

      try{
        const res = await fetch('http://127.0.0.1:5000/login', {
          method:'POST', headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ name: nimi, password: salasana, player_id })
        });
        const data = await res.json().catch(()=>({}));
        if(res.ok){
          alert('Kirjautuminen onnistui!');
          try{ localStorage.setItem('user_name', nimi); localStorage.setItem('player_id', player_id); localStorage.setItem('difficulty', vaikeus); }catch(e){}
          window.location.href = 'home.html';
        } else {
          alert(data.error || 'Kirjautuminen epäonnistui');
        }
      }catch(err){
        console.error(err); alert('Yhteysvirhe palvelimeen');
      }
    });

    nimiEl.addEventListener('input', ()=>{ if(playerIdEl.disabled){ lockPlayerId(false); } });

    playerIdEl.addEventListener('dblclick', ()=>{ if(playerIdEl.disabled) { if(confirm('Haluatko vapauttaa Player ID:n muokkausta varten?')) lockPlayerId(false); } });

    if(salasanaEl.value.trim()){
      playerArea.style.display = 'flex'; populateSuggestions();
    }

    const signupModal = document.getElementById('signupModal');
    const adminModal = document.getElementById('adminModal');
    document.getElementById('signupBtn').addEventListener('click', ()=>{ signupModal.style.display='flex'; signupModal.setAttribute('aria-hidden','false'); });
    document.getElementById('adminBtn').addEventListener('click', ()=>{ adminModal.style.display='flex'; adminModal.setAttribute('aria-hidden','false'); });
    document.getElementById('su_cancel').addEventListener('click', ()=>{ signupModal.style.display='none'; signupModal.setAttribute('aria-hidden','true'); });
    document.getElementById('ad_cancel').addEventListener('click', ()=>{ adminModal.style.display='none'; adminModal.setAttribute('aria-hidden','true'); });

    document.getElementById('su_create').addEventListener('click', async ()=>{
      const name = document.getElementById('su_name').value.trim();
      const age = document.getElementById('su_age').value.trim();
      const pass = document.getElementById('su_pass').value.trim();
      if(!name || !age || !pass) { alert('Täytä kaikki kentät'); return; }
      try{
        const res = await fetch('http://127.0.0.1:5000/signup', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ name, age, password: pass }) });
        const data = await res.json().catch(()=>({}));
        if(res.ok){ alert('Tili luotu onnistuneesti!'); signupModal.style.display='none'; } else { alert(data.error || 'Virhe tilin luonnissa'); }
      }catch(e){ console.error(e); alert('Yhteysvirhe palvelimeen'); }
    });

    document.getElementById('ad_login').addEventListener('click', async ()=>{
      const u = document.getElementById('ad_user').value.trim();
      const p = document.getElementById('ad_pass').value.trim();
      if(!u||!p){ alert('Täytä käyttäjätunnus ja salasana'); return; }
      try{
        const res = await fetch('http://127.0.0.1:5000/admin-login',{ method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ username:u, password:p }) });
        const data = await res.json().catch(()=>({}));
        if(data.message){ alert(data.message); window.location.href='admin.html'; } else { alert(data.error || 'Kirjautuminen epäonnistui'); }
      }catch(e){ console.error(e); alert('Yhteysvirhe palvelimeen'); }
    });

    window.addEventListener('click', (ev)=>{
      if(ev.target===signupModal){ signupModal.style.display='none'; signupModal.setAttribute('aria-hidden','true'); }
      if(ev.target===adminModal){ adminModal.style.display='none'; adminModal.setAttribute('aria-hidden','true'); }
    });

    playerIdEl.addEventListener('focus', ()=>{ if(playerArea.style.display!=='none' && suggestionsEl.children.length===0) populateSuggestions(); });
