async function checkEligibility() {
    const studentID = document.getElementById('studentID').value;

    if (!studentID) {
        alert("Please enter a valid Student ID!");
        return;
    }

    try {
        const detailsResponse = await fetch(`http://localhost:3000/get_student_details?student_id=${studentID}`);
        const detailsData = await detailsResponse.json();

        if (detailsData.error) {
            alert(detailsData.error);
            return;
        }

        const scholarshipResponse = await fetch(`http://localhost:3000/check_scholarship?student_id=${studentID}`);
        const scholarshipData = await scholarshipResponse.json();

        const examResponse = await fetch(`http://localhost:3000/check_exam_permission?student_id=${studentID}`);
        const examData = await examResponse.json();

        const resultsContainer = document.getElementById('results');
        resultsContainer.style.display = 'block';

        document.getElementById('studentIDDisplay').innerHTML = `<strong>Student ID:</strong> ${detailsData.student_id}`;
        document.getElementById('studentCGPADisplay').innerHTML = `<strong>CGPA:</strong> ${detailsData.cgpa}`;
        document.getElementById('studentAttendanceDisplay').innerHTML = `<strong>Attendance:</strong> ${detailsData.attendance}%`;

        const scholarshipStatus = document.getElementById('scholarshipStatus');
        scholarshipStatus.innerText = scholarshipData.status === "eligible" 
            ? "Eligible for Scholarship" 
            : "Not Eligible for Scholarship";
        scholarshipStatus.className = `status ${scholarshipData.status === "eligible" ? "positive" : "negative"}`;

        const examPermissionStatus = document.getElementById('examPermissionStatus');
        examPermissionStatus.innerText = examData.status === "permitted" 
            ? "Permitted for Exam" 
            : "Not Permitted for Exam";
        examPermissionStatus.className = `status ${examData.status === "permitted" ? "positive" : "negative"}`;

    } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to fetch eligibility data. Please ensure the server is running.");
    }
}
