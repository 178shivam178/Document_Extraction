import os
import csv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)

from dotenv import load_dotenv

load_dotenv() 
api_key = os.getenv("OPENAI_API_KEY")
    
def set_openai_api_key():
    os.environ["OPENAI_API_KEY"] = api_key


def writingCSVFile(extracted_field, filename):
    try:
        csv_filename = "{}.csv".format(filename)
        csv_path = os.path.join("extracted_output/", csv_filename)
        merged_dict = {**extracted_field}
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(merged_dict.keys())
            writer.writerow(merged_dict.values())
    except Exception as e:
        print(f"Error while writing to CSV: {e}")

def get_text_chunks(text):
    try:
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks
    except Exception as e:
        print(f"Error while splitting text: {e}")
        return []

def get_vectorstore(text_chunks):
    try:
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vectorstore
    except Exception as e:
        print(f"Error while creating vectorstore: {e}")
        return None

def get_conversation_chain(vectorstore):
    try:
        llm = ChatOpenAI()
        memory = ConversationBufferMemory(
            memory_key='chat_history', return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory
        )
        return conversation_chain
    except Exception as e:
        print(f"Error while creating conversation chain: {e}")
        return None

def Invoice_Extract(conversation):
    try:
        user_questions = [
            "What is the invoice number?",
            "What is invoice date?", 
            "What is due date?",
            "What is the balance due?",
            "What is total amount?",
            "What is the Vendor name", 
            "What is Pay term?", 
            "What is the PO number?",
            "What is total Service/Product name?", 
            "What is the Bank account number?", 
            "What is Tax id ?",
            "What is Tax rate?", 
            "What is the Discount?", 
            "What is Billing address?", 
            "What is Shipping address ?",
            "What is Shipping method?", 
            "What is the Cost center or GL for Service vendors?", 
            "What is Sub total?",
            "What is the Tax amount with rate of %?", 
            "What is Remarks/Notes ?"
        ]

        keys = [
            'Invoice_Number', 
            'Invoice_date', 
            'Due_Date', 
            'Balance_Due', 
            'Total_Amount',
            'Vendor_Name',
            'Pay_Term', 
            'PO_Number', 
            'Product_Name', 
            'Bank_account_number', 
            'Tax_id',
            'Tax_rate', 
            'Discount', 
            'Billing_address', 
            'Shipping address', 
            'Shipping_method', 
            'Cost_Center',
            'Sub_Total', 
            'Tax_amount', 
            'Remarks'
        ]

        negation_words = ["not", "n't", "no", "none", "neither", "cannot", "can't"]

        extracted_fields = dict.fromkeys(keys)

        for i, user_question in enumerate(user_questions):
            response = conversation({'question': user_question})
            answer = response['answer']
            negation_present = any(word.lower() in answer.lower() for word in negation_words)
            if negation_present:
                extracted_fields[keys[i]] = None
            else:
                info_start = answer.find("is") + 3
                extracted_fields[keys[i]] = answer[info_start:]
        return extracted_fields
    except Exception as e:
        print(f"Error while extracting invoice details: {e}")
        return None


def PO_Extract(conversation):
    try:
        user_questions = [
            "What is the Vendor name?",
            "What is the Date?",
            "What is the Address?",
            "What is the P.O number?",
            "What is the Payment terms?",
            "What is the Rate?",
            "What is the P.O validity?",
            "What is the Qty?",
            "What is the Ship Via/Shipping method?",
            "What is the Purchases from - Vendor name with address & contact name?",
            "What is the Ship to company name with address & contact name?",
            "What is the Goods required by date?",
            "What are the Item descriptions?",
            "What is the Quantity?",
            "What is the Unit Price?",
            "What is the Amount?",
            "What is the Approved by?",
            "What is the Subtotal?",
            "What are the Freight charges?",
            "What is the Sales tax?",
            "What is the Order Total with currency?",
            "What are the Remarks/Notes?"
            ]
        keys = [
            'Vendor_Name',
            'Date',
            'Address',
            'P.O_Number',
            'Payment_Terms',
            'Rate',
            'P.O_Validity',
            'Qty',
            'Shipping_Method',
            'Purchases_From',
            'Ship_To',
            'Goods_Required_By',
            'Item_Descriptions',
            'Quantity',
            'Unit_Price',
            'Amount',
            'Approved_By',
            'Subtotal',
            'Freight_Charges',
            'Sales_Tax',
            'Order_Total',
            'Remarks'
            ]
        negation_words = ["not", "n't", "no", "none", "neither", "cannot", "can't"]

        extracted_fields = dict.fromkeys(keys)

        for i, user_question in enumerate(user_questions):
            response = conversation({'question': user_question})
            answer = response['answer']
            negation_present = any(word.lower() in answer.lower() for word in negation_words)
            if negation_present:
                extracted_fields[keys[i]] = None
            else:
                info_start = answer.find("is") + 3
                extracted_fields[keys[i]] = answer[info_start:]
        return extracted_fields
    except Exception as e:
        print(f"Error while extracting invoice details: {e}")
        return None

def PR_Extract(conversation):
    try:
        user_questions = [
            "What is the PR Number?",
            "What is the PR Date?",
            "What is the Expected date of delivery?",
            "What is the Qty?",
            "What is the Description?",
            "What is the Product/Service?",
            "What are the Price details/Budgeted cost?",
            "What are the Quotations/Tender received?",
            "Who is the Recommended vendor?",
            "Who proposed this with signature & date?",
            "Who approved this with signature & date?",
            "What is the Department?",
            "What is the Expense account?",
            "Where is it to be shipped (Ship To)?",
            "What are the Remarks?"
            ]
        keys = [
            'PR_Number',
            'PR_Date',
            'Expected_Delivery_Date',
            'Qty',
            'Description',
            'Product_Service',
            'Price_Details_Budgeted_Cost',
            'Quotations_Tender_Received',
            'Recommended_Vendor',
            'Proposed_By',
            'Approved_By',
            'Department',
            'Expense_Account',
            'Ship_To',
            'Remarks'
            ]
        negation_words = ["not", "n't", "no", "none", "neither", "cannot", "can't"]

        extracted_fields = dict.fromkeys(keys)

        for i, user_question in enumerate(user_questions):
            response = conversation({'question': user_question})
            answer = response['answer']
            negation_present = any(word.lower() in answer.lower() for word in negation_words)
            if negation_present:
                extracted_fields[keys[i]] = None
            else:
                info_start = answer.find("is") + 3
                extracted_fields[keys[i]] = answer[info_start:]
        return extracted_fields
    except Exception as e:
        print(f"Error while extracting invoice details: {e}")
        return None
      
def Form9(conversation):
    try:
        user_questions = [
            "What is the Vendor name?",
            "What is the Business name?",
            "What is the Vendor class?",
            "What is the Address?",
            "What is the SSN/EIN?",
            "Who is the Signature of authorized person?",
            "What is the Date?"
            ]
        keys = [
            'Vendor_Name',
            'Business_Name',
            'Vendor_Class',
            'Address',
            'SSN_EIN',
            'Authorized_Person_Signature',
            'Date'
            ]

        negation_words = ["not", "n't", "no", "none", "neither", "cannot", "can't"]

        extracted_fields = dict.fromkeys(keys)

        for i, user_question in enumerate(user_questions):
            response = conversation({'question': user_question})
            answer = response['answer']
            negation_present = any(word.lower() in answer.lower() for word in negation_words)
            if negation_present:
                extracted_fields[keys[i]] = None
            else:
                info_start = answer.find("is") + 3
                extracted_fields[keys[i]] = answer[info_start:]
        return extracted_fields
    except Exception as e:
        print(f"Error while extracting invoice details: {e}")
        return None
    
def FormW8BEN(conversation):
    try:
        user_questions = [
            "What is the Name?",
            "What is the Address?",
            "What is the SSN/TIN?",
            "What is the Foreign TIN?",
            "What is the Resident country?",
            "What are the Special rates and conditions %?",
            "What is the Certification?",
            "What is the Date?"
            ]
        keys = [
            'Name',
            'Address',
            'SSN_TIN',
            'Foreign_TIN',
            'Resident_Country',
            'Special_Rates_and_Conditions',
            'Certification',
            'Date'
            ]
        negation_words = ["not", "n't", "no", "none", "neither", "cannot", "can't"]

        extracted_fields = dict.fromkeys(keys)

        for i, user_question in enumerate(user_questions):
            response = conversation({'question': user_question})
            answer = response['answer']
            negation_present = any(word.lower() in answer.lower() for word in negation_words)
            if negation_present:
                extracted_fields[keys[i]] = None
            else:
                info_start = answer.find("is") + 3
                extracted_fields[keys[i]] = answer[info_start:]
        return extracted_fields
    except Exception as e:
        print(f"Error while extracting invoice details: {e}")
        return None

def FormW8BENE(conversation):
    try:
        user_questions = [
            "What is the Name?",
            "What is the Name of disregarded entity?",
            "What is the Country of incorporation?",
            "What is the Entity type?",
            "What is the FATCA status?",
            "What is the Permanent address?",
            "What are the Treaty benefits?",
            "What is the Certification?",
            "What is the Date?"
            ]
        keys = [
            'Name',
            'Disregarded_Entity_Name',
            'Country_of_Incorporation',
            'Entity_Type',
            'FATCA_Status',
            'Permanent_Address',
            'Treaty_Benefits',
            'Certification',
            'Date'
            ]

        negation_words = ["not", "n't", "no", "none", "neither", "cannot", "can't"]

        extracted_fields = dict.fromkeys(keys)

        for i, user_question in enumerate(user_questions):
            response = conversation({'question': user_question})
            answer = response['answer']
            negation_present = any(word.lower() in answer.lower() for word in negation_words)
            if negation_present:
                extracted_fields[keys[i]] = None
            else:
                info_start = answer.find("is") + 3
                extracted_fields[keys[i]] = answer[info_start:]
        return extracted_fields
    except Exception as e:
        print(f"Error while extracting invoice details: {e}")
        return None
    
def GRGN(conversation):
    try:
        user_questions = [
            "What is the GRN No.?",
            "What is the Vendor/Supplier Name with address?",
            "What is the Buyer/Recipient name and address?",
            "What is the Date?",
            "What is the Location?",
            "What is the Purchase Order?",
            "What is the Delivery Method?",
            "What are the Item descriptions?",
            "What is the Price (in currency)?",
            "What is the Tax (in currency value)?",
            "Who received the goods?",
            "What is the Date of receipt?",
            "What are the Charging details (Cost center/Account codes)?",
            "What is the Department name?",
            "Do you have any Additional Information?"
            ]
        keys = [
            'GRN_No',
            'Vendor_Supplier_Name_Address',
            'Buyer_Recipient_Name_Address',
            'Date',
            'Location',
            'Purchase_Order',
            'Delivery_Method',
            'Item_Descriptions',
            'Price_in_Currency',
            'Tax_in_Currency_Value',
            'Goods_Received_By',
            'Date_of_Receipt',
            'Charging_Details',
            'Department_Name',
            'Additional_Information'
            ]
        negation_words = ["not", "n't", "no", "none", "neither", "cannot", "can't"]

        extracted_fields = dict.fromkeys(keys)

        for i, user_question in enumerate(user_questions):
            response = conversation({'question': user_question})
            answer = response['answer']
            negation_present = any(word.lower() in answer.lower() for word in negation_words)
            if negation_present:
                extracted_fields[keys[i]] = None
            else:
                info_start = answer.find("is") + 3
                extracted_fields[keys[i]] = answer[info_start:]
        return extracted_fields
    except Exception as e:
        print(f"Error while extracting invoice details: {e}")
        return None
    
def Unknown(conversation):
    try:
        user_questions = [
            'what are the imp information present in text?'
            ]
        keys = [
            'Information'
            ]
        negation_words = ["not", "n't", "no", "none", "neither", "cannot", "can't"]

        extracted_fields = dict.fromkeys(keys)

        for i, user_question in enumerate(user_questions):
            response = conversation({'question': user_question})
            answer = response['answer']
            negation_present = any(word.lower() in answer.lower() for word in negation_words)
            if negation_present:
                extracted_fields[keys[i]] = None
            else:
                info_start = answer.find("is") + 3
                extracted_fields[keys[i]] = answer[info_start:]
        return extracted_fields
    except Exception as e:
        print(f"Error while extracting invoice details: {e}")
        return None
    
def detect_document_type(text):
    invoice_keywords = ["invoice"]
    po_keywords = ["purchase order"]
    pr_keywords = ["purchase requisitions","purchase requisition","purchase request"]
    form9_keywords = ["w-9"]
    formW8BEN_keywords = ["w-8ben"]
    formW8BENE_keywords = ["w-8ben-e"]
    grgn_keywords = ["goods receipt note", "delivery note","goods received note"]
    text = text[0:200]
    first_line = text.lower()

    if any(keyword in first_line for keyword in invoice_keywords):
        return "Invoice"
    elif any(keyword in first_line for keyword in po_keywords):
        return "Purchase_Order"
    elif any(keyword in first_line for keyword in pr_keywords):
        return "Purchase_Requisition"
    elif any(keyword in first_line for keyword in form9_keywords):
        return "Form9"
    elif any(keyword in first_line for keyword in formW8BEN_keywords):
        return "FormW_8BEN"
    elif any(keyword in first_line for keyword in formW8BENE_keywords):
        return "FormW_8BEN_E"
    elif any(keyword in first_line for keyword in grgn_keywords):
        return "Goods_Receipt_Note"
    else:
        return "Unknown"

def CheckInvoice(raw_text):
    try:
        set_openai_api_key()

        document_type = detect_document_type(raw_text)
        print(document_type)
        if not document_type:
            return {'error': 'No ducument_type found.'}
        
        text_chunks = get_text_chunks(raw_text)
        if not text_chunks:
            return {'error': 'No text chunks found.'}
        
        vectorstore = get_vectorstore(text_chunks)
        if vectorstore is None:
            return {'error': 'Failed to create vectorstore.'}
        
        conversation = get_conversation_chain(vectorstore)
        if conversation is None:
            return {'error': 'Failed to create conversation chain.'}
        
        if document_type == "Invoice":
                extraction_function = Invoice_Extract

        elif document_type == "Purchase_Order":
                extraction_function = PO_Extract

        elif document_type == "Purchase_Requisition":
                extraction_function = PR_Extract

        elif document_type == "Form9":
                extraction_function = Form9

        elif document_type == "FormW_8BEN":
                extraction_function = FormW8BEN

        elif document_type == "FormW_8BEN_E":
                extraction_function = FormW8BENE

        elif document_type == "Goods_Receipt_Note":
                extraction_function = GRGN
        
        elif document_type == "Unknown":
                extraction_function = Unknown

        else:
            return {'error': 'Failed to extract ducument type.'}
        
        extracted_fields = extraction_function(conversation)
        
        if extracted_fields is not None:
            return extracted_fields,document_type
        else:
            return {'error': 'Failed to extract invoice details.'}
    except Exception as e:
        return {'error': 'An error occurred', 'details': str(e)}

