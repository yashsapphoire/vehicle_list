import streamlit as st
import json
import os
from typing import Dict, List
import uuid

# File path for storing vehicle data
VEHICLES_FILE = "vehicles.json"

# Initialize default session state values
st.session_state.setdefault("editing", False)
st.session_state.setdefault("edit_id", None)
st.session_state.setdefault("make", "")
st.session_state.setdefault("model", "")
st.session_state.setdefault("variant", "")
st.session_state.setdefault("vehicle_name", "")

def migrate_data(vehicles: List[Dict]) -> List[Dict]:
    """Migrate old data format to new format"""
    migrated_vehicles = []
    for vehicle in vehicles:
        migrated_vehicle = {
            "id": vehicle.get("id", str(uuid.uuid4())),
            "make": vehicle.get("make", ""),
            "model": vehicle.get("model", ""),
            "variant": vehicle.get("variant", ""),
            "vehicle_name": vehicle.get("vehicle_name", "")
        }
        migrated_vehicles.append(migrated_vehicle)
    return migrated_vehicles

def load_vehicles() -> List[Dict]:
    """Load vehicles from JSON file"""
    if os.path.exists(VEHICLES_FILE):
        with open(VEHICLES_FILE, 'r') as f:
            vehicles = json.load(f)
            # Migrate data to new format
            vehicles = migrate_data(vehicles)
            # Save migrated data
            save_vehicles(vehicles)
            return vehicles
    return []

def save_vehicles(vehicles: List[Dict]):
    """Save vehicles to JSON file"""
    with open(VEHICLES_FILE, 'w') as f:
        json.dump(vehicles, f, indent=4)

def add_vehicle(make: str, model: str, variant: str, vehicle_name: str):
    """Add a new vehicle to the list"""
    vehicles = load_vehicles()
    new_vehicle = {
        "id": str(uuid.uuid4()),
        "make": make,
        "model": model,
        "variant": variant,
        "vehicle_name": vehicle_name
    }
    vehicles.append(new_vehicle)
    save_vehicles(vehicles)

def update_vehicle(vehicle_id: str, make: str, model: str, variant: str, vehicle_name: str):
    """Update an existing vehicle"""
    vehicles = load_vehicles()
    for vehicle in vehicles:
        if vehicle["id"] == vehicle_id:
            vehicle["make"] = make
            vehicle["model"] = model
            vehicle["variant"] = variant
            vehicle["vehicle_name"] = vehicle_name
            break
    save_vehicles(vehicles)

def delete_vehicle(vehicle_id: str):
    """Delete a vehicle"""
    vehicles = load_vehicles()
    vehicles = [v for v in vehicles if v["id"] != vehicle_id]
    save_vehicles(vehicles)

def reset_form():
    """Reset form fields"""
    st.session_state.make = ""
    st.session_state.model = ""
    st.session_state.variant = ""
    st.session_state.vehicle_name = ""
    st.session_state.editing = False
    st.session_state.edit_id = None

# Streamlit UI
st.title("Vehicle Management Dashboard")

# Input form
with st.form("vehicle_form"):
    make = st.text_input("Make", value=st.session_state.make)
    model = st.text_input("Model", value=st.session_state.model)
    variant = st.text_input("Variant", value=st.session_state.variant)
    vehicle_name = st.text_input("Vehicle Name", value=st.session_state.vehicle_name)
    
    if st.session_state.editing:
        submit_button = st.form_submit_button("Update Vehicle")
        if submit_button and make and model:
            update_vehicle(st.session_state.edit_id, make, model, variant, vehicle_name)
            reset_form()
            st.success("Vehicle updated successfully!")
            st.rerun()
    else:
        submit_button = st.form_submit_button("Add Vehicle")
        if submit_button and make and model:
            add_vehicle(make, model, variant, vehicle_name)
            reset_form()
            st.success("Vehicle added successfully!")
            st.rerun()

# Display vehicles
st.subheader("Vehicle List")
vehicles = load_vehicles()

if not vehicles:
    st.info("No vehicles added yet.")
else:
    for vehicle in vehicles:
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 1, 1])
        
        with col1:
            st.write(f"**Make:** {vehicle.get('make', 'N/A')}")
        with col2:
            st.write(f"**Model:** {vehicle.get('model', 'N/A')}")
        with col3:
            st.write(f"**Variant:** {vehicle.get('variant', 'N/A')}")
        with col4:
            st.write(f"**Vehicle Name:** {vehicle.get('vehicle_name', 'N/A')}")
        with col5:
            if st.button("Edit", key=f"edit_{vehicle['id']}"):
                st.session_state.editing = True
                st.session_state.edit_id = vehicle['id']
                st.session_state.make = vehicle.get('make', '')
                st.session_state.model = vehicle.get('model', '')
                st.session_state.variant = vehicle.get('variant', '')
                st.session_state.vehicle_name = vehicle.get('vehicle_name', '')
                st.rerun()
        with col6:
            if st.button("Delete", key=f"delete_{vehicle['id']}"):
                delete_vehicle(vehicle['id'])
                st.success("Vehicle deleted successfully!")
                st.rerun()
        st.divider()
