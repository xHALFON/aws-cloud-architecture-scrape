import React, { useState } from "react";
import Modal from "./Modal";

const ArchitectureItem = ({ architecture }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isParsedContent, setIsParsedContent] = useState(true);

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleString("he-IL", {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const renderCloudFormationContent = (content) => {
    return (
      <div className="cloudformation-content">
        {content.AWSTemplateFormatVersion && (
          <div className="cf-section">
            <span className="label">Template Version: </span>
            <span>{content.AWSTemplateFormatVersion}</span>
          </div>
        )}

        {content.Parameters && (
          <div className="cf-section">
            <h5>Parameters</h5>
            <div className="cf-grid">
              {Object.entries(content.Parameters).map(([key, value]) => (
                <div key={key} className="cf-item">
                  <span className="cf-key">{key}</span>
                  <span className="cf-value">{JSON.stringify(value)}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {content.Resources && (
          <div className="cf-section">
            <h5>Resources</h5>
            <div className="cf-grid">
              {Object.entries(content.Resources).map(([key, value]) => (
                <div key={key} className="cf-item">
                  <span className="cf-key">{key}</span>
                  <span className="cf-type">{value.Type}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {content.Outputs && (
          <div className="cf-section">
            <h5>Outputs</h5>
            <div className="cf-grid">
              {Object.entries(content.Outputs).map(([key, value]) => (
                <div key={key} className="cf-item">
                  <span className="cf-key">{key}</span>
                  <span className="cf-value">{JSON.stringify(value)}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  const renderSimpleContent = (content) => {
    return (
      <>
        <p className="content-summary">{content.summary}</p>
        {(content.detected_services?.length > 0 ||
          content.resources?.length > 0) && (
          <div className="services-section">
            <span className="label">Detected Services: </span>
            <div className="service-tags">
              {content.detected_services?.map((service, index) => (
                <span key={`service-${index}`} className="service-tag">
                  {service}
                </span>
              ))}
              {content.resources?.map((service, index) => (
                <span key={`resource-${index}`} className="service-tag">
                  {service}
                </span>
              ))}
            </div>
          </div>
        )}
      </>
    );
  };

  const isCloudFormationTemplate = (content) => {
    return content && content.AWSTemplateFormatVersion;
  };

  const renderCardContent = () => {
    const services = architecture.parsed_content?.detected_services || [];
    const resources = architecture.parsed_content?.resources || [];
    const allServices = [...services, ...resources];

    return (
      <>
        <h3 className="card-title">{architecture.title || "No Title"}</h3>
        <div className="card-timestamp">
          {formatDate(architecture.timestamp)}
        </div>
        {allServices.length > 0 && (
          <div className="card-services">
            {allServices.slice(0, 3).map((service, index) => (
              <span key={index} className="card-service-tag">
                {service}
              </span>
            ))}
            {allServices.length > 3 && (
              <span className="card-service-more">
                +{allServices.length - 3}
              </span>
            )}
          </div>
        )}
      </>
    );
  };

  return (
    <>
      <div className="architecture-card" onClick={() => setIsModalOpen(true)}>
        {renderCardContent()}
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
        <div className="modal-header">
          <h2>{architecture.title || "No Title"}</h2>
          <span className="timestamp">
            {formatDate(architecture.timestamp)}
          </span>
        </div>

        <div className="modal-body">
          <div className="detail-section">
            <h4>Source Information</h4>
            <p>
              <strong>Type:</strong> {architecture.source_type}
            </p>
            <p>
              <strong>URL:</strong>{" "}
              <a
                href={architecture.source_url}
                target="_blank"
                rel="noopener noreferrer"
              >
                {architecture.source_url}
              </a>
            </p>
          </div>

          {architecture.description && (
            <div className="detail-section">
              <h4>Description</h4>
              <p>{architecture.description}</p>
            </div>
          )}

          <div className="detail-section">
            <h4>Content</h4>
            <div className="content-tabs">
              <div className="tab-buttons">
                <button
                  className={`tab-button ${isParsedContent ? "active" : ""}`}
                  onClick={() => setIsParsedContent(true)}
                >
                  Parsed Content
                </button>
                <button
                  className={`tab-button ${!isParsedContent ? "active" : ""}`}
                  onClick={() => setIsParsedContent(false)}
                >
                  Raw Content
                </button>
              </div>
              <div className="tab-content">
                {isParsedContent ? (
                  <div className="parsed-content">
                    {isCloudFormationTemplate(architecture.parsed_content)
                      ? renderCloudFormationContent(architecture.parsed_content)
                      : renderSimpleContent(architecture.parsed_content)}
                  </div>
                ) : (
                  <pre className="raw-content">{architecture.raw_content}</pre>
                )}
              </div>
            </div>
          </div>
        </div>
      </Modal>
    </>
  );
};

export default ArchitectureItem;
