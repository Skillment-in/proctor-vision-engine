function checkViolations() {
  fetch('/latest_violation')
    .then(res => res.json())
    .then(data => {
      if (data.violation) {
        let popup = document.getElementById('popup');
        popup.innerText = `⚠️ Violation: ${data.violation}`;
        popup.style.display = 'block';
        setTimeout(() => popup.style.display = 'none', 5000);
      }
    });
}

setInterval(checkViolations, 3000);
