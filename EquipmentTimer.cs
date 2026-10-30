using UnityEngine;
using HMLLibrary;
using UltimateWater;
using System.Reflection;

public class EquipmentTimer : Mod
{
    private GUIStyle style;
    private Network_Player playerNetwork;
    private PlayerEquipment playerEquipment;

    // Reflection
    private FieldInfo equipmentField;
    private FieldInfo equippedField;
    private FieldInfo equippedSlotField;
    private FieldInfo itemInstanceField;

    public void Start()
    {
        style = new GUIStyle();
        style.fontSize = 24;
        style.normal.textColor = Color.white;

        equipmentField = typeof(PlayerEquipment).GetField(
            "equipment",
            BindingFlags.NonPublic | BindingFlags.Instance);

        equippedField = typeof(Equipment).GetField(
            "equipped",
            BindingFlags.NonPublic | BindingFlags.Instance);

        equippedSlotField = typeof(Equipment).GetField(
            "equippedSlot",
            BindingFlags.NonPublic | BindingFlags.Instance);

        itemInstanceField = typeof(Slot).GetField(
            "itemInstance",
            BindingFlags.NonPublic | BindingFlags.Public | BindingFlags.Instance);
    }

    public void Update()
    {
        if (playerNetwork == null)
            playerNetwork = ComponentManager<Network_Player>.Value;

        if (playerEquipment == null)
            playerEquipment = UnityEngine.Object.FindObjectOfType<PlayerEquipment>();
    }

    private string FormatTime(int uses)
    {
        if (uses < 0)
            uses = 0;

        int minutes = uses / 60;
        int seconds = uses % 60;

        return $"{minutes}:{seconds:00}";
    }

    public void OnGUI()
    {
        if (playerNetwork == null || playerNetwork.PersonController == null)
            return;

        // 물속에서만 표시
        if (playerNetwork.PersonController.SubmersionState != SubmersionState.Full)
            return;

        if (playerEquipment == null)
            return;

        Equipment[] equipments =
            (Equipment[])equipmentField.GetValue(playerEquipment);

        int y = 50; // 오른쪽 위 시작 위치

        foreach (Equipment eq in equipments)
        {
            if (eq == null)
                continue;

            bool equipped = (bool)equippedField.GetValue(eq);
            if (!equipped)
                continue;

            string uniqueName = eq.equipableItem.UniqueName;
            string displayName;

            if (uniqueName == "Flipper")
                displayName = "오리발";
            else if (uniqueName == "OxygenBottle")
                displayName = "산소통";
            else
                continue;

            Slot_Equip slot =
                (Slot_Equip)equippedSlotField.GetValue(eq);

            if (slot == null || slot.IsEmpty)
                continue;

            ItemInstance instance =
                (ItemInstance)itemInstanceField.GetValue(slot);

            if (instance == null)
                continue;

            int uses = instance.Uses;
            string text = $"{displayName} {FormatTime(uses)}";

            // 글자 색
            Color textColor = Color.white;
            if (uses <= 30)
                textColor = Color.red;
            else if (uses <= 60)
                textColor = Color.yellow;

            float x = Screen.width - 240;

            // 그림자
            GUI.color = Color.black;
            GUI.Label(new Rect(x + 2, y + 2, 220, 30), text, style);

            // 본문
            GUI.color = textColor;
            GUI.Label(new Rect(x, y, 220, 30), text, style);

            y += 30;
        }

        GUI.color = Color.white;
    }

    public void OnModUnload()
    {
        UnityEngine.Debug.Log("EquipmentTimer unloaded!");
    }
}