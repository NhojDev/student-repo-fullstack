const port = process.env.PORT || 5001;

// http://localhost:5001/form should return a form with input elements for username, email, and submit button

// http://localhost:5001/submit should return all the data the user entered

const express = require("express");
const app = express();

app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.status(200);
  res.set({ 'Content-Type': 'text/html' });
  res.send('Form Exercise');
});

app.get("/form", (req, res) => {
  res.status(200); 
  res.set({ "Content-Type": "text/html" });

  res.send(`
    <form action="/submit" method="post">
    <label for="username">Username:</label>
    <input type="text" id="username" name="username" required>
    <br><br>


    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required>
    <br><br>


    <input type="submit" value="Submit">
    </form>
  `);
});


app.post("/submit", (req, res) => {
  const { username, email } = req.body;
  res.status(200);
  res.set({ "Content-Type": "text/html" });

  res.send(`
    <h1>Form Submitted Successfully</h1>
    <p><strong>Username:</strong> ${username}</p>
    <p><strong>Email:</strong> ${email}</p>
  `);
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
