
document.addEventListener('DOMContentLoaded',function(){var start=new Date();var dcIdentifier=Array.from(document.querySelectorAll('meta[name]')).find(function(meta){var name=meta.getAttribute('name');var scheme=meta.getAttribute('scheme');return(name&&name.toLowerCase()==='dc.identifier'&&(!scheme||scheme.toLowerCase()==='doi'));});if(dcIdentifier){var doi=dcIdentifier.getAttribute('content');window.addEventListener('pagehide',function(){var end=new Date();var duration=end-start;var xhr=new XMLHttpRequest();xhr.open('POST','/action/analytics?EventType=FullTextDuration&Duration='+duration+'&DOI='+doi,true);xhr.send();});window.addEventListener('afterprint',function(){var xhr=new XMLHttpRequest();xhr.open('POST','/action/analytics?EventType=FullTextPrint&DOI='+doi,true);xhr.send();});}});

