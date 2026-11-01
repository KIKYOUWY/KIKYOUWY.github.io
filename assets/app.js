const profile=JSON.parse(document.getElementById('profile-data').textContent);
const root=document.documentElement;
const language=document.getElementById('language');
const theme=document.getElementById('theme');
let filter='selected';
const papers=[...document.querySelectorAll('.paper')];
const search=document.getElementById('paper-search');
function save(key,value){try{localStorage.setItem(key,value)}catch{}}
function filterPapers(){
  const query=search.value.trim().toLocaleLowerCase();let count=0;
  for(const paper of papers){
    const match=filter==='all'||(filter==='selected'?paper.dataset.selected==='true':paper.dataset.year===filter);
    paper.hidden=!(match&&paper.textContent.toLocaleLowerCase().includes(query));
    if(!paper.hidden)count++;
  }
  document.querySelectorAll('[data-group]').forEach(heading=>{
    heading.hidden=!papers.some(paper=>!paper.hidden&&paper.dataset.category===heading.dataset.group);
  });
  document.getElementById('results-count').textContent=root.lang==='zh'?`显示 ${count} / ${papers.length} 篇论文 · 本人姓名已加粗`:`Showing ${count} of ${papers.length} publications · My name is highlighted`;
  document.getElementById('no-results').hidden=count!==0;
}
function updateLanguage(){
  const zh=root.lang==='zh';language.textContent=zh?'EN':'中文';
  language.setAttribute('aria-label',zh?'Switch to English':'切换为中文');
  search.placeholder=zh?'搜索论文…':'Search publications…';
  document.getElementById('copy-citation').textContent=zh?'复制 BibTeX':'Copy BibTeX';
  document.getElementById('download-citation').textContent=zh?'下载 .bib':'Download .bib';
  filterPapers();
}
language.addEventListener('click',()=>{root.lang=root.lang==='zh'?'en':'zh';save('yw-lang',root.lang);updateLanguage()});
function updateTheme(){theme.setAttribute('aria-pressed',String(root.dataset.theme==='dark'))}
theme.addEventListener('click',()=>{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';save('yw-theme',root.dataset.theme);updateTheme()});
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{
  filter=button.dataset.filter;
  document.querySelectorAll('[data-filter]').forEach(b=>{const active=b===button;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active))});
  filterPapers();
}));
search.addEventListener('input',filterPapers);
const dialog=document.getElementById('citation-dialog');
let currentCitation='';let downloadUrl=null;
function bibEscape(text){return String(text).replaceAll('\\','\\textbackslash{}').replace(/([&%$#_])/g,'\\$1')}
function getBib(paper){
  // Preserve Scholar's author spelling instead of inventing expanded names.
  const authors=paper.authors.split(/,\s*|，\s*/).map(s=>s.trim()).filter(Boolean).join(' and ');
  const type=paper.category==='conference'?'inproceedings':paper.category==='preprint'?'misc':'article';
  const fields={title:`{${bibEscape(paper.title)}}`,author:bibEscape(authors),year:paper.year};
  if(paper.venue)fields[paper.category==='conference'?'booktitle':paper.category==='preprint'?'howpublished':'journal']=bibEscape(paper.venue);
  if(paper.doi)fields.doi=paper.doi;
  fields.url=paper.doi?`https://doi.org/${paper.doi}`:paper.scholar;
  if(paper.category==='preprint')fields.note='Preprint';
  return `@${type}{wan${paper.year}${paper.id.replaceAll('-','')},\n`+Object.entries(fields).map(([key,value])=>`  ${key} = {${value}}`).join(',\n')+'\n}';
}
document.querySelectorAll('.cite').forEach(button=>button.addEventListener('click',()=>{
  const paper=profile.papers.find(p=>p.id===button.dataset.id);currentCitation=getBib(paper);
  document.getElementById('citation-text').textContent=currentCitation;
  document.getElementById('copy-status').textContent='';
  if(downloadUrl)URL.revokeObjectURL(downloadUrl);
  downloadUrl=URL.createObjectURL(new Blob([currentCitation],{type:'text/plain;charset=utf-8'}));
  const download=document.getElementById('download-citation');download.href=downloadUrl;download.download=`${paper.id}.bib`;
  dialog.showModal();
}));
document.getElementById('close-citation').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',event=>{if(event.target===dialog){const rect=dialog.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)dialog.close()}});
document.getElementById('copy-citation').addEventListener('click',async()=>{
  const status=document.getElementById('copy-status');
  try{await navigator.clipboard.writeText(currentCitation);status.textContent=root.lang==='zh'?'已复制到剪贴板。':'Copied to clipboard.'}
  catch{const range=document.createRange();range.selectNodeContents(document.getElementById('citation-text'));const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);status.textContent=root.lang==='zh'?'请按 Ctrl+C 复制，或下载 .bib 文件。':'Press Ctrl+C to copy, or download the .bib file.'}
});
updateLanguage();updateTheme();
const figureDialog=document.getElementById('figure-dialog');
const figureImage=document.getElementById('figure-large');
const figureSize=document.getElementById('figure-size');
document.querySelectorAll('[data-figure]').forEach(link=>link.addEventListener('click',event=>{
  if(event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
  const paper=profile.papers.find(p=>p.id===link.dataset.figure);
  event.preventDefault();
  figureDialog.classList.remove('original-size');figureSize.setAttribute('aria-pressed','false');
  document.getElementById('figure-title').textContent=paper.title;
  figureImage.src=link.href;figureImage.alt=paper.image_caption||paper.title;
  document.getElementById('figure-caption').textContent=paper.image_caption||'';
  document.getElementById('figure-original').href=link.href;
  const source=document.getElementById('figure-source');
  source.href=paper.image_source||paper.scholar;
  figureDialog.showModal();
}));
figureSize.addEventListener('click',()=>{
  const original=figureDialog.classList.toggle('original-size');figureSize.setAttribute('aria-pressed',String(original));
});
document.getElementById('close-figure').addEventListener('click',()=>figureDialog.close());
figureDialog.addEventListener('click',event=>{
  if(event.target===figureDialog){const rect=figureDialog.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)figureDialog.close()}
});
const observer=new IntersectionObserver(entries=>{for(const entry of entries){if(entry.isIntersecting){document.querySelectorAll('.nav-links a').forEach(a=>a.classList.toggle('active',a.hash===`#${entry.target.id}`))}}},{rootMargin:'-15% 0px -65% 0px'});
document.querySelectorAll('main>section[id]').forEach(section=>observer.observe(section));
