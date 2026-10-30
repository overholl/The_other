using UnityEngine;
using HMLLibrary;

public class BruceRespawnTimer : Mod
{
    private AI_StateMachine_Shark shark;

    private float respawnTimer = 0f;

    // 5분 + 3분 전체 타이머
    private bool fullTimerRunning = false;

    // 시체가 사라진 후 3분 타이머
    private bool respawnCounting = false;

    private GUIStyle style;

    public void Start()
    {
        style = new GUIStyle();
        style.fontSize = 24;
        style.normal.textColor = Color.white;
    }

    public void Update()
    {
        // ==============================
        // 3분 부활 타이머
        // ==============================
        if (respawnCounting)
        {
            respawnTimer += Time.deltaTime;

            if (respawnTimer >= 180f)
            {
                respawnCounting = false;
                respawnTimer = 0f;
                shark = null;
            }

            return;
        }

        // ==============================
        // 5분 + 3분 전체 타이머
        // ==============================
        if (fullTimerRunning)
        {
            respawnTimer += Time.deltaTime;

            // 시체가 사라짐
            if (shark == null)
            {
                fullTimerRunning = false;

                // 즉시 3분 타이머 시작
                respawnCounting = true;
                respawnTimer = 0f;

                return;
            }

            return;
        }

        // ==============================
        // Bruce 찾기
        // ==============================
        if (shark == null)
        {
            AI_StateMachine_Shark[] sharks =
                UnityEngine.Object.FindObjectsOfType<AI_StateMachine_Shark>();

            if (sharks.Length > 0)
            {
                shark = sharks[0];
            }

            return;
        }

        // ==============================
        // Bruce 사망 감지
        // ==============================
        if (shark.currentState is AI_State_Dead)
        {
            // 죽는 순간부터 8분 타이머 시작
            respawnTimer = 0f;
            fullTimerRunning = true;
        }
    }

    public void OnGUI()
    {
        if (!fullTimerRunning && !respawnCounting)
            return;

        float remaining;

        if (respawnCounting)
        {
            // 시체 제거 후 3분
            remaining = 180f - respawnTimer;
        }
        else
        {
            // 사망 후 8분
            remaining = 480f - respawnTimer;
        }

        if (remaining < 0f)
            remaining = 0f;

        int seconds = Mathf.CeilToInt(remaining);

        GUI.Label(
            new Rect(
                Screen.width - 320f,
                20f,
                300f,
                40f
            ),
            "상어 리스폰 " + seconds + "초",
            style
        );
    }

    public void OnModUnload()
    {
        UnityEngine.Debug.Log("BruceRespawnTimer has been unloaded!");
    }
}