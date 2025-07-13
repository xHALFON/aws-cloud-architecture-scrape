import React from "react";

const ExampleUrls = ({ onUrlClick }) => {
  const examples = [
    {
      type: "Image",
      url: "https://images.edrawmax.com/examples/aws-architecture-diagram-examples/example-2.png",
    },
    {
      type: "Image",
      url: "https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/solutions/approved/images/06744048-8a02-433b-b499-a3b1521cd4d4-aws-advanced-cloud-observability-intelligence-dashboards-architecture-diagram-2792x1151.706193a8f163764e24724ad9a01b680f82736ed0.png",
    },
    {
      type: "Html",
      url: "https://raw.githubusercontent.com/aws-quickstart/quickstart-examples/refs/heads/main/samples/ec2-instance-connect/ec2-instance-connection-example.yaml",
    },
    {
      type: "Json",
      url: "https://raw.githubusercontent.com/TechPrimers/aws-cloud-formation-templates/master/templates/aws-cf-ec2-s3.json",
    },
  ];

  return (
    <div className="example-urls">
      <h3>Example URLs for Scraping</h3>
      <div className="example-cards">
        {examples.map((example, index) => (
          <div
            key={index}
            className="example-card"
            onClick={() => onUrlClick(example.url)}
          >
            <div className="example-type">{example.type}</div>
            <div className="example-url">{example.url}</div>
            <button className="copy-button">Use This URL</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ExampleUrls;
