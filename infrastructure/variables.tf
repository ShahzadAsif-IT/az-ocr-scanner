variable "storage_account_name" {
  description = "Azure Storage Account Name"
  type        = string
  default     = "azocrblobsaasif20250802"
}

variable "resource_group_name" {
    description = "Azure Resource Group Name"
    type        = string
    default     = "az-ocr-scanner-rg"
}

variable "azure_region" {
    description = "Azure Region"
    type        = string
    default     = "East US 2 "
}

variable "computer_vision_name" {
    description = "Azure Cognitive Service for Computer Vision"
    type        = string
    default     = "az-ocr-scanner-cv"
}

variable "openai_account_name" {
    description = "OpenAI Account Name"
    type        = string
    default     = "az-ocr-scanner-openai-acct"
}

variable "project_name" {
    description = "Project Name"
    type        = string
    default     = "az-ocr-scanner"
}

variable "subscription_id" {
    description = "Subscription Id"
    type        = string
    default     = "<Your Azure Subscription Id>"
}