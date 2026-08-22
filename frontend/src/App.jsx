import "./App.css";
import ChatWidget from "./components/ChatWidget.jsx";

const STATS = [
  { num: "11", label: "Happy clients" },
  { num: "16", label: "Projects completed" },
  { num: "7", label: "Years of data experience" },
  { num: "18", label: "Certified specialists" },
];

const SERVICES = [
  { name: "BI & Data Analytics", desc: "Collecting and analysing data to give you clear, actionable insight." },
  { name: "Data Fabric & Big Data Engineering", desc: "Seamless, real-time integration across your big data systems." },
  { name: "Data Ops & Governance", desc: "Automated, governed data operations built into how you work." },
  { name: "Data Science", desc: "Extracting actionable insight from raw data." },
  { name: "Audit CAATs & Data Processes", desc: "Computer-assisted audit techniques to test your systems' integrity." },
  { name: "Systems Development", desc: "Building, upgrading or replacing the systems that run your business." },
];

export default function App() {
  return (
    <div className="page">
      <nav className="nav">
        <div className="brand">
          AG<span>.</span>
        </div>
        <div className="navlinks">
          <span>About</span>
          <span>Services</span>
          <span>Contact</span>
        </div>
      </nav>

      <header className="hero">
        <div className="eyebrow">Data Alchemy, Applied</div>
        <h1>
          Turn big data into a <em>competitive advantage</em>.
        </h1>
        <p className="lede">
          Analytics Group partners with businesses across South Africa to turn raw data into
          credible, useful insight &mdash; through BI &amp; analytics, data engineering,
          governance, data science, audit CAATs and systems development.
        </p>
        <p className="quote">&ldquo;In God we trust. All others must bring data.&rdquo;</p>
        <div className="cta-row">
          <button className="btn-gold">Book a consultation</button>
          <button className="btn-ghost">Explore services</button>
        </div>
      </header>

      <section className="stats">
        {STATS.map((s) => (
          <div className="stat" key={s.label}>
            <div className="num">{s.num}</div>
            <div className="label">{s.label}</div>
          </div>
        ))}
      </section>

      <section className="services">
        <h2>Our services</h2>
        <div className="service-grid">
          {SERVICES.map((s) => (
            <div className="service-card" key={s.name}>
              <h3>{s.name}</h3>
              <p>{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Floating assistant, ready to guide any visitor through the above */}
      <ChatWidget />
    </div>
  );
}
