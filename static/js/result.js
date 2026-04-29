

const studentResults = [
  {
    year: "2025-2026",
    class: "Sem 1",
    division: "Section A",
    session: "EVEN 2025-2026",
    exam: "Mid Term",
    marks: "Math: 80 | CS: 85 | English: 75",
    grade: "A"
  },
  {
    year: "2025-2026",
    class: "Sem 5",
    division: "Section B",
    session: "ODD 2025-2026",
    exam: "End Term",
    marks: "DBMS: 90 | Java: 88 | OS: 85",
    grade: "A+"
  }
];

function getResult() {
  const year = document.getElementById("year").value;
  const cls = document.getElementById("class").value;
  const division = document.getElementById("division").value;
  const session = document.getElementById("session").value;
  const exam = document.getElementById("exam").value.trim();

  const resultBox = document.getElementById("resultBox");
  const resultText = document.getElementById("resultText");

  resultBox.classList.remove("hidden");

  // Find matching result
  const found = studentResults.find(data =>
    data.year === year &&
    data.class === cls &&
    data.division === division &&
    data.session === session &&
    data.exam.toLowerCase() === exam.toLowerCase()
  );

  if (found) {
    resultBox.style.background = "#e6ffed";
    resultText.style.color = "green";

    resultText.innerHTML = `
      ✅ Result Found <br><br>
      📘 Class: ${found.class} <br>
      📝 Exam: ${found.exam} <br>
      📊 Marks: ${found.marks} <br>
      🏆 Grade: ${found.grade}
    `;
  } else {
    resultBox.style.background = "#ffe6e6";
    resultText.style.color = "red";

    resultText.innerText = "❌ No Data Found !!!";
  }
}