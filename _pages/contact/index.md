---
layout: page
title: Contact
permalink: /contact/
toggle: on
rank: 7
---
<head>
    <script>UPLOADCARE_PUBLIC_KEY = "9ece2f24515da2c6390d";</script>
<script src="https://ucarecdn.com/libs/widget/2.10.2/uploadcare.full.min.js" charset="utf-8"></script>
</head>
<H3>We always welcome applications for postdoctoral fellowship positions</H3>
Diversity is an integral part of Canadian history, culture, and identity. In the Morin laboratory, we strive to maintain an equitable and inclusive culture where all forms of diversity are seen as added value in the unifying goal of reducing the impact of cancer. 

<form class="wj-contact" action="https://formspree.io/{{site.email}}" method="POST">
    <input type="email" name="email" placeholder="Enter your email"><br>
  First name:<br>
  <input type="text" name="firstname"><br>
  Last name:<br>
  <input type="text" name="lastname">
  Interested in:<br>
  <input type="radio" name="application goal" value="MSc"> MSc<br>
  <input type="radio" name="application goal" value="PhD"> PhD<br>
  <input type="radio" name="application goal" value="Postdoctoral"> Postdoctoral fellow<br>
  <input type="radio" name="application goal" value="Work"> Employment <br>
  <input type="radio" name="application goal" value="Volunteer"> Volunteer
  <br>
  <textarea rows="10" cols="150" name="message" placeholder="Type your message here"></textarea>
  Attach a single file (CV, coverletter). Merge multiple files into one PDF.<br> <input type="hidden" role="uploadcare-uploader" name="myFile" />
  <button type="submit">Send</button>
</form>

<style>
form.wj-contact input[type="text"], form.wj-contact textarea[type="text"] {
    width: 100%;
    vertical-align: middle;
    margin-top: 0.25em;
    margin-bottom: 0.5em;
    padding: 0.75em;
    font-family: monospace, sans-serif;
    font-weight: lighter;
    border-style: solid;
    border-color: #444;
    outline-color: #2e83e6;
    border-width: 1px;
    border-radius: 3px;
    transition: box-shadow .2s ease;
}
form.wj-contact input[type="submit"] {
    outline: none;
    color: white;
    background-color: #2e83e6;
    border-radius: 3px;
    padding: 0.5em;
    margin: 0.25em 0 0 0;
    border: 1px solid transparent;
    height: auto;
}
</style>

