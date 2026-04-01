<div style="font-family: 'Outfit', sans-serif; background: radial-gradient(circle at 10% 20%, #0a192f 0%, #0d1f3a 90%); color: #f1faee; padding: 40px; border-radius: 12px; border: 1px solid #457b9d; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">

<!-- SLIDE 1: TITLE -->
<div style="text-align: center; padding: 100px 0;">
  <div style="font-size: 80px; margin-bottom: 20px;">🛡️</div>
  <h1 style="color: #e63946; font-size: 60px; margin: 0; border-bottom: 5px solid #457b9d; display: inline-block; padding-bottom: 10px;">VitalStream Study Guide</h1>
  <p style="font-size: 28px; color: #a8dadc; margin-top: 20px;">Week 06: Capstone Implementation & Recovery</p>
  <div style="margin-top: 40px; font-size: 20px; color: #f1faee; opacity: 0.8;">
    <p>Lead Architect: <strong>Rob Chich</strong></p>
    <p>Phase 2 | Secure Architecture Design</p>
  </div>
</div>

<hr style="border: 0; border-top: 2px solid rgba(168, 218, 220, 0.2); margin: 60px 0;">

<!-- SLIDE 2: LESSON 1 -->
<div style="margin-bottom: 100px;">
  <div style="display: flex; align-items: center; margin-bottom: 30px;">
    <div style="font-size: 40px; margin-right: 20px;">🚀</div>
    <h2 style="color: #e63946; font-size: 42px; margin: 0;">Lesson 1: Automated Deployment Proof</h2>
  </div>
  <p style="font-size: 24px; line-height: 1.6; margin-bottom: 30px;">
    Successfully transformed our deployment logic into a <strong>Zero-Human-Intervention</strong> script. We demonstrated that even in a highly isolated environment (Private Subnet), infrastructure can be deployed and verified with 100% reliability.
  </p>
  <div style="background: #0d1b2a; padding: 20px; border-radius: 8px; border-left: 10px solid #e63946;">
    <img src="file:///d:/download_other/AWS/2026%20Cloud%20Security%20Architect%20Roadmap/assets/screenshot_deployment.png" style="width: 100%; border-radius: 4px; border: 1px solid #457b9d;" alt="Deployment Script Output">
    <p style="text-align: center; margin-top: 15px; font-style: italic; color: #a8dadc;">Evidence: 100% completion in App Tier Subnet</p>
  </div>
</div>

<!-- SLIDE 3: LESSON 2/3 -->
<div style="margin-bottom: 100px;">
  <div style="display: flex; align-items: center; margin-bottom: 30px;">
    <div style="font-size: 40px; margin-right: 20px;">🗺️</div>
    <h2 style="color: #e63946; font-size: 42px; margin: 0;">Lesson 2 & 3: Network Integrity</h2>
  </div>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px;">
    <div>
      <h3 style="color: #a8dadc;">Visual Security Audits</h3>
      <p style="font-size: 20px;">The VPC Resource Map serves as our <strong>Primary Defense Layer</strong>. We verified:</p>
      <ul style="font-size: 18px; line-height: 1.8;">
        <li><span style="color: #e63946;">●</span> Isolated Route Tables (No IGW for Private Tiers)</li>
        <li><span style="color: #e63946;">●</span> Hardened Subnet Associations</li>
        <li><span style="color: #e63946;">●</span> Administrative Bastion Bridge Connectivity</li>
      </ul>
    </div>
    <div style="background: rgba(168, 218, 220, 0.05); padding: 10px; border-radius: 8px;">
      <img src="file:///d:/download_other/AWS/2026%20Cloud%20Security%20Architect%20Roadmap/assets/screenshot_vpc_map.png" style="width: 100%; border-radius: 4px;" alt="VPC Resource Map">
    </div>
  </div>
</div>

<!-- SLIDE 4: LESSON 4/5 -->
<div style="margin-bottom: 100px;">
  <div style="display: flex; align-items: center; margin-bottom: 30px;">
    <div style="font-size: 40px; margin-right: 20px;">🌉</div>
    <h2 style="color: #e63946; font-size: 42px; margin: 0;">Lesson 4 & 5: The Security Bridge</h2>
  </div>
  <p style="font-size: 24px; line-height: 1.6;">
    Managing private instances requires an <strong>Administrative Airlock</strong>. By deploying the Bastion and solving Windows SSH permission errors (icacls), we secured our administrative path without compromising data isolation.
  </p>
  <div style="margin-top: 30px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
    <div style="background: #1d3557; padding: 20px; border-radius: 8px; border: 1px solid #457b9d;">
      <p style="color: #a8dadc; font-weight: bold;">Problem</p>
      <p style="font-size: 18px;">SSM Parameter "None" errors and Key Permission timeouts.</p>
    </div>
    <div style="background: #e63946; padding: 20px; border-radius: 8px; border: 1px solid #457b9d; color: white;">
      <p style="font-weight: bold;">Solution</p>
      <p style="font-size: 18px;">Automated Fallbacks & Local Privilege Hardening (chmod 400 equivalent).</p>
    </div>
  </div>
</div>

<!-- SLIDE 5: THE FINAL PORTAL -->
<div style="margin-bottom: 100px;">
  <div style="display: flex; align-items: center; margin-bottom: 30px;">
    <div style="font-size: 40px; margin-right: 20px;">📊</div>
    <h2 style="color: #e63946; font-size: 42px; margin: 0;">Lesson 6: State-of-the-Art Dashboard</h2>
  </div>
  <p style="font-size: 24px; line-height: 1.6; margin-bottom: 40px;">
    Infrastructure is only as strong as its usability. We delivered a <strong>High-Fidelity Medical Dashboard</strong> with Glassmorphism effects and automated data injection.
  </p>
  <div style="position: relative;">
     <img src="file:///d:/download_other/AWS/2026%20Cloud%20Security%20Architect%20Roadmap/assets/portal_mockup.png" style="width: 100%; border-radius: 12px; box-shadow: 0 0 50px rgba(230, 57, 70, 0.4); border: 1px solid #e63946;" alt="VitalStream Portal">
     <div style="position: absolute; bottom: 30px; left: 30px; background: rgba(10, 25, 47, 0.9); padding: 20px; border-left: 5px solid #e63946; border-radius: 4px;">
       <p style="margin: 0; font-size: 20px; color: #a8dadc;">Design Specs:</p>
       <p style="margin: 5px 0 0 0; font-size: 16px;">Glassmorphism | Dark Mode | FontAwesome | Bootstrap Grid</p>
     </div>
  </div>
</div>

<!-- SLIDE 6: GOVERNANCE -->
<div style="text-align: center; border: 2px solid #e63946; padding: 50px; border-radius: 20px; background: rgba(230, 57, 70, 0.05);">
  <h2 style="color: #e63946; font-size: 42px;">Session Governance Complete</h2>
  <div style="display: flex; justify-content: space-around; margin-top: 40px;">
    <div>
      <div style="font-size: 32px; font-weight: bold;">$20.00</div>
      <p style="color: #a8dadc;">Monthly Cap Locked</p>
    </div>
    <div>
      <div style="font-size: 32px; font-weight: bold;">100%</div>
      <p style="color: #a8dadc;">Resources Audited/Cleaned</p>
    </div>
    <div>
      <div style="font-size: 32px; font-weight: bold;">0</div>
      <p style="color: #a8dadc;">Z-Trust Violations</p>
    </div>
  </div>
  <blockquote style="margin-top: 40px; border-left: 10px solid #a8dadc; background: rgba(168, 218, 220, 0.1); padding: 20px; font-style: italic;">
    "Architecture is not just what it looks like, it's how it stays standing under pressure."
  </blockquote>
</div>

<footer style="margin-top: 60px; text-align: right; color: #a8dadc; font-size: 14px; opacity: 0.6;">
  Final Submission | Phase 2 Recovery | 2026 Cloud Security Architect Roadmap
</footer>

</div>
