import streamlit as st
from datetime import datetime, timedelta
import pytz
import tensorflow as tf

# Load your trained model
model = tf.keras.models.load_model('model.h5')

# Function to predict traffic based on the nearest 15 minutes
def predict_traffic(day, time_str):
    time = datetime.strptime(time_str, '%H:%M:%S').time()
    rounded_time = datetime.combine(datetime.today(), time)
    rounded_time = rounded_time - timedelta(minutes=rounded_time.minute % 15, seconds=rounded_time.second, microseconds=rounded_time.microsecond)
    
    # Prepare the input for the model
    # Assuming your model takes input as [day, hour, minute]
    day_num = datetime.strptime(day, '%A').weekday()  # Convert day to numerical representation
    hour = rounded_time.hour
    minute = rounded_time.minute
    
    # Example input for the model
    model_input = [[day_num, hour, minute]]
    
    # Predict traffic
    prediction = model.predict(model_input)
    
    # Return a formatted string with prediction
    return f"Predicted traffic for {day} at {rounded_time.time()} is {prediction[0][0]}"

# Function to get current time prediction
def get_current_prediction():
    now = datetime.now(pytz.timezone('Your/Timezone'))  # Adjust timezone accordingly
    current_day = now.strftime('%A').lower()  # e.g., 'sunday'
    current_time = now.strftime('%H:%M:%S')
    return predict_traffic(current_day, current_time)

# Streamlit UI
def main():
    st.title("Traffic Prediction System")
    
    # Display current traffic prediction
    st.subheader("Current Traffic Situation")
    current_prediction = get_current_prediction()
    st.write(current_prediction)

    # User input for custom prediction
    st.subheader("Custom Traffic Prediction")
    
    day = st.selectbox(
        "Select Day",
        ("sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday")
    )
    
    time_str = st.text_input("Enter Time (HH:MM:SS)", value=datetime.now().strftime('%H:%M:%S'))
    
    if st.button("Predict Traffic"):
        custom_prediction = predict_traffic(day, time_str)
        st.write(custom_prediction)

if __name__ == "__main__":
    main()
